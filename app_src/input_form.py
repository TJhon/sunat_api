import streamlit as st


def form_input():
    hscode = st.text_input(
        "HScode (10 digitos) o un identificador (Opcional)",
    )
    col1, col2 = st.columns(2)
    default = {"value": None, "placeholder": "123.123"}

    units = col1.number_input("Unidades totales", **default)
    unit_price = col2.number_input("Precio unitario", **default)
    cbm = col1.number_input("Volumen del producto (CBM)", **default)
    total_kg = col2.number_input("Cantidad de Kg totales", **default)
    province = col1.checkbox("Es de Provincia?")
    first_import = col2.checkbox("Primera Importacion?")
    values = {
        "hscode": hscode,
        "units": units,
        "price_unit": unit_price,
        "cbm": cbm,
        "total_kg": total_kg,
        "province": province,
        "first_import": first_import,
    }
    return values
