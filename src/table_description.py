from selenium import webdriver
from selenium.webdriver.common.by import By

from src.utils import clean_hs
from tqdm import tqdm

import pandas as pd
import warnings

warnings.filterwarnings("ignore")


ref_hs = pd.read_csv("./hs_code.csv")
hs_codes = ref_hs["hs_code"].values

url = "http://www.aduanet.gob.pe/itarancel/arancelS01Alias"
browser = webdriver.Chrome()
browser.get(url)


hs = "2935500000"


def get_info_table(
    browser,
    hs,
    id_frame1="descripcionFrame",
    id_frame2="descripcionFrame22",
    body_table="/html/body/div/center/table/tbody",
):
    description = browser.find_element(By.ID, id_frame1)
    browser.switch_to.frame(description)
    table = browser.find_element(By.ID, id_frame2)
    browser.switch_to.frame(table)
    tbody = browser.find_element(By.XPATH, body_table)
    data = []

    for tr in tbody.find_elements(By.XPATH, "//tr"):
        row = [x.text for x in tr.find_elements(By.XPATH, ".//td")]
        data.append(row)

    data = pd.DataFrame(data).transpose().reset_index(drop=True)
    data.columns = data.iloc[0]
    data = data[1:]
    data["hs_code"] = hs

    browser.switch_to.default_content()
    browser.switch_to.default_content()

    return data


def consult_hs(
    hs,
    browser=browser,
    hs_input="/html/body/form/div/table/tbody/tr[1]/td/input[1]",
    consult_click="/html/body/form/div/table/tbody/tr[3]/td/input[1]",
):
    hs = clean_hs(hs)
    browser.find_element(By.XPATH, hs_input).send_keys(hs)
    browser.find_element(By.XPATH, consult_click).click()
    browser.find_element(By.XPATH, hs_input).clear()

    data = get_info_table(browser, hs)
    return data


full_data = pd.DataFrame()
name_data = "./data/taxes.csv"
e = []

for i in tqdm(hs_codes):
    try:
        row_data = consult_hs(i)
        full_data = pd.concat([full_data, row_data])
        full_data.to_csv(name_data, index=False)

    except:
        e.append(i)

pd.DataFrame({"errors": e}).to_csv("errors_hs_code.csv")
