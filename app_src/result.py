import requests, pandas as pd, streamlit as st

user = "alguien"

taxes = [
    "hscode",
    "fob",
    "insurage",
    "cif",
    "igv",
    "ipm",
    "antidupping",
    "perception",
    "total_taxes",
]

logistic = [
    "hscode",
    "freight",
    "desconsolidation",
    "transport_local",
    "province_transport",
    "total_logistic",
]


def metrics(column, metric_name, data=None, ref=st, symbol=" $", value=None, more=None):
    if value is None:
        total = data[column].sum()
    else:
        total = value
    totalstr = str(total) + symbol
    ref.metric(metric_name, totalstr, more)


def sum_fixed(ref: dict):
    total = 0
    for key in list(ref.keys()):
        if key == "tc":
            continue
        total += ref[key]
    return total


def result(user, fixed_cost):
    url = f"http://127.0.0.1:8000/user_cotization/{user}"
    data = requests.get(url).json()
    data = pd.DataFrame(data).round(2)
    taxes_df = data[taxes]
    logistic_df = data[logistic]
    logistic_value = data["total_logistic"].sum()
    logistic_cost_fixed = sum_fixed(fixed_cost)
    total_logistic = round(logistic_value + logistic_cost_fixed, 2)
    total_taxes = data["total_taxes"].sum()
    total_fob = data["fob"].sum()
    total_valor = total_taxes + total_fob + total_logistic

    # st.write(fixed_cost.keys())
    relacion = round(total_valor / total_fob * 100, 2)
    relacion = str(relacion) + " %"

    metrics("", "Valor de la Importacion", value=total_valor, more=relacion)
    col1, col2, col3 = st.columns(3)

    metrics("total_taxes", "Total Impuestos", data, ref=col3)
    metrics("fob", "Total FOB", data, ref=col1)
    metrics("", "Total Logistica ", ref=col2, value=total_logistic)
    metrics("total_logistic", "Logistica ", data, ref=col2)
    metrics("", "Logistica (Costos Fijos)", ref=col2, value=logistic_cost_fixed)
    # col1.metric(taxes_df["total_taxes"].sum())

    with st.expander("Impuestos"):
        st.dataframe(taxes_df)
    with st.expander("Costos Logisticos"):
        st.dataframe(logistic_df)
