import streamlit as st

from services.alertas_service import (
    generar_alertas_indagacion,
    generar_alertas_juicio,
    generar_alertas_ordenes_pj,
    procesar_alertas_pendientes
)

st.title(
    "⚙️ Generador de Alertas"
)

if st.button(
    "Generar Alertas de Indagación"
):

    generar_alertas_indagacion()

    st.success(
        "✅ Alertas generadas."
    )

if st.button(
    "Generar Alertas de Juicio"
):

    generar_alertas_juicio()

    st.success(
        "✅ Alertas de juicio generadas."
    )

if st.button(
    "Generar Alertas de Órdenes PJ"
):

    generar_alertas_ordenes_pj()

    st.success(
        "✅ Alertas de Órdenes PJ generadas."
    )

if st.button(
    "Procesar Alertas Pendientes"
):

    procesar_alertas_pendientes()

    st.success(
        "✅ Alertas procesadas."
    )