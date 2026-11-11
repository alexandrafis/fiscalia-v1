import streamlit as st

from datetime import timedelta

from services.juicios_service import (
    obtener_casos_indagacion,
    trasladar_a_juicio
)

st.title("⚖️ Traslado de Indagación a Juicio")

casos = obtener_casos_indagacion()

if not casos:

    st.warning(
        "No existen casos en etapa de INDAGACIÓN."
    )

    st.stop()

casos_dict = {
    fila.radicado: fila
    for fila in casos
}

radicado = st.selectbox(
    "Seleccione Caso",
    list(casos_dict.keys())
)

caso = casos_dict[radicado]

st.info(
    f"Etapa Actual: {caso.etapa_actual}"
)

st.info(
    f"Pena Máxima Registrada: "
    f"{caso.pena_maxima_meses} meses"
)

tipo_actuacion = st.radio(
    "Tipo de Actuación",
    [
        "IMPUTACION",
        "ACUSACION"
    ]
)

fecha_actuacion = st.date_input(
    "Fecha de Actuación"
)

mitad_pena = int(
    caso.pena_maxima_meses / 2
)

if mitad_pena < 36:
    mitad_pena = 36

fecha_prescripcion_juicio = (
    fecha_actuacion +
    timedelta(days=mitad_pena * 30)
)

st.success(
    f"Prescripción Art. 292 CPP: "
    f"{fecha_prescripcion_juicio}"
)

if st.button(
    "⚖️ Trasladar a Juicio"
):

    trasladar_a_juicio(
        caso.id,
        tipo_actuacion,
        fecha_actuacion,
        fecha_prescripcion_juicio
    )

    st.success(
        "Caso trasladado correctamente a JUICIO"
    )

    st.rerun()