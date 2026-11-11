import streamlit as st

from services.configuracion_alertas_service import (
    obtener_configuracion,
    guardar_configuracion
)

st.title(
    "⚙️ Configuración de Alertas"
)

config = obtener_configuracion()

correo = st.text_input(
    "Correo para recibir alertas",
    value=config.correo_destino
)

st.divider()

st.subheader(
    "🔍 Alertas de Indagación"
)

indagacion_1 = st.number_input(
    "Primer aviso",
    value=config.indagacion_1
)

indagacion_2 = st.number_input(
    "Segundo aviso",
    value=config.indagacion_2
)

indagacion_3 = st.number_input(
    "Tercer aviso",
    value=config.indagacion_3
)

indagacion_4 = st.number_input(
    "Cuarto aviso",
    value=config.indagacion_4
)

st.divider()

st.subheader(
    "⚖️ Alertas de Juicio"
)

juicio_1 = st.number_input(
    "Primer aviso juicio",
    value=config.juicio_1
)

juicio_2 = st.number_input(
    "Segundo aviso juicio",
    value=config.juicio_2
)

juicio_3 = st.number_input(
    "Tercer aviso juicio",
    value=config.juicio_3
)

juicio_4 = st.number_input(
    "Cuarto aviso juicio",
    value=config.juicio_4
)

st.divider()

st.subheader(
    "📋 Alertas Órdenes PJ"
)

alerta_orden_1 = st.number_input(
    "Primer aviso orden",
    value=config.alerta_orden_1
)

alerta_orden_2 = st.number_input(
    "Segundo aviso orden",
    value=config.alerta_orden_2
)

alerta_orden_3 = st.number_input(
    "Tercer aviso orden",
    value=config.alerta_orden_3
)

alerta_orden_4 = st.number_input(
    "Cuarto aviso orden",
    value=config.alerta_orden_4
)

st.divider()

if st.button(
    "💾 Guardar Configuración"
):

    guardar_configuracion(
        correo,

        indagacion_1,
        indagacion_2,
        indagacion_3,
        indagacion_4,

        juicio_1,
        juicio_2,
        juicio_3,
        juicio_4,

        alerta_orden_1,
        alerta_orden_2,
        alerta_orden_3,
        alerta_orden_4
    )

    st.success(
        "✅ Configuración guardada correctamente."
    )