from bs4 import BeautifulSoup
import requests, re, pandas as pd

url = "http://www.aduanet.gob.pe/itarancel/arancelS01Alias"

params = {"accion": "buscarPartida", "esframe": "1"}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cookie": "ITARANCELTEMPSESSION=Hhy9l1RBRMwQJy4j2fs6N1j95vyRZY8vGvKqvljCBhSJF4zMvTySlVS7nL6j1v4Spk8YDqwvr7yG7zwyZJZG6yQmQRTcQLXTFJpsWm6gH0ZVdZm2yMr2gGpPPr2vzM127hV2zjckkjzv5lDYN1jYpYKNq8JWMyhqHnV5xFfJQjVdjQnQv7Lvrm1DyQrNKFLFF2lbXygdRlsyGhhLWrxTPxMQYRJ9PMP1lJplR51hxPmyLwsw1WTVvVjpCJvSXykX!-1136956652!-554657031; TS01577d4a=014dc399cbee749fac94cc19e93f3f93c2061053d27ac3bb99f3118cd11eba7e122bf90bb5e06ec21d00cfb89035def94aa5f61d873016b1273e28480442baacb3a85f6962",
    "Host": "www.aduanet.gob.pe",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
}

content = requests.get(url, params=params, headers=headers)


# html to table

soup = BeautifulSoup(content.text, "html.parser")
table = soup.find("table")

hs = []
texts = []
rows = table.find_all("tr")[1:]

for row in rows:
    fila = row.find_all("td")
    hs_code = re.search(r"goPartida\('(\d+)'\)", fila[0].find("a")["href"]).group(1)
    description_text = fila[1].get_text(strip=True)

    hs.append(hs_code)
    texts.append(description_text)


pd.DataFrame({"hs_code": hs, "descrip": texts}).to_csv("hs_code.csv", index=False)

if __name__ == "main":
    pass
