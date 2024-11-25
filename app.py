import streamlit as st, pandas as pd
import requests
from dataclasses import asdict


from app_src.input_form import form_input
from app_src.sidebar import taxes, cost_volumen, other_parameters

from app_src.result import result

from src.Information import InputForm, FixedCostTotal, VariableCosts, TaxesHSCode, Info


st.title("Calculo de Importaciones (LCL)")
user = st.text_input("Usuario que Registra", value="Alguien")
register, summary = st.tabs(["Registro del Producto", "Resumen"])

with st.sidebar:
    st.title("Modificar Parametros")
    tax = taxes()
    volumen = cost_volumen()
    other = other_parameters()

with register:
    inputs = form_input()
    inputs["user"] = user

    url_post = "http://127.0.0.1:8000/"
    if st.button("Registrar Producto"):
        description = asdict(InputForm(**inputs))
        others_d = asdict(FixedCostTotal(**other))
        volume_d = asdict(VariableCosts(**volumen))
        tax_d = asdict(TaxesHSCode(**tax))

        data_dict = {**inputs, **other, **tax, **volumen}
        result = Info(**data_dict).summary()
        # st.write(result)
        requests.post(url_post + "cotization_values/", json=data_dict)
        requests.post(url_post + "cotization_result/", json=result)
        st.success(f"Registro completo del hs de codigo: `{result['hscode']}`")

    # data =


with summary:
    if st.button("Calcular Resumen", use_container_width=True, type="primary"):

        result(user, other)
