import streamlit as st
import pandas as pd

from datetime import date
from datetime import timedelta

from services.juicios_service import (
    obtener_juicios,
    guardar_datos_juicio,
    obtener_datos_caso_juicio
)

from services.casos_service import (
    registrar_sentencia
)

st.title(
    "⚖️ Control de Juicios"
)

juicios = obtener_juicios()

if not juicios:

    st.warning(
        "No existen juicios registrados."
    )

    st.stop()

datos = []

for fila in juicios:

    if fila.fecha_prescripcion_juicio is None:

        dias_restantes = 9999

    else:

        dias_restantes = (
            fila.fecha_prescripcion_juicio -
            date.today()
        ).days

    semaforo = "🟢 VERDE"

    if dias_restantes <= 0:
        semaforo = "⚫ PRESCRITO"

    elif dias_restantes <= 30:
        semaforo = "🔴 ROJO"

    elif dias_restantes <= 90:
        semaforo = "🟠 NARANJA"

    elif dias_restantes <= 180:
        semaforo = "🟡 AMARILLO"

    datos.append(
        [
            fila.radicado,
            fila.tipo_actuacion,
            fila.fecha_inicio_prescripcion,
            fila.fecha_prescripcion_juicio,
            fila.estado_juicio,
            semaforo
        ]
    )

df = pd.DataFrame(
    datos,
    columns=[
        "RADICADO",
        "TIPO ACTUACION",
        "INICIO PRESCRIPCION",
        "PRESCRIPCION JUICIO",
        "ESTADO",
        "SEMAFORO"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

st.metric(
    "Total Juicios Activos",
    len(df)
)

st.subheader(
    "📝 Completar Datos del Juicio"
)

radicado_juicio = st.selectbox(
    "Seleccione Juicio",
    df["RADICADO"].tolist(),
    key="juicio_datos"
)

datos_caso = obtener_datos_caso_juicio(
    radicado_juicio
)

pena_maxima = datos_caso.pena_maxima_meses

st.info(
    f"Pena Máxima Registrada: {pena_maxima} meses"
)

fecha_imputacion = st.date_input(
    "Fecha de Imputación"
)

fecha_acusacion = st.date_input(
    "Fecha de Acusación"
)

tipo_actuacion = st.selectbox(
    "Tipo de Actuación",
    [
        "IMPUTACION",
        "ACUSACION"
    ]
)

mitad_pena = int(
    pena_maxima / 2
)

if mitad_pena < 36:

    mitad_pena = 36

if mitad_pena > 120:

    mitad_pena = 120

fecha_prescripcion_juicio = (
    fecha_acusacion +
    timedelta(days=mitad_pena * 30)
)

st.success(
    f"""
Prescripción Juicio: {fecha_prescripcion_juicio}

Meses aplicados: {mitad_pena}
"""
)

if st.button(
    "💾 Guardar Datos Juicio"
):

    guardar_datos_juicio(
        radicado_juicio,
        fecha_imputacion,
        fecha_acusacion,
        tipo_actuacion,
        fecha_prescripcion_juicio
    )

    st.success(
        "Datos del juicio actualizados correctamente"
    )

    st.rerun()

st.divider()

st.subheader(
    "⚖️ Finalizar Juicio"
)

radicado_sentencia = st.selectbox(
    "Seleccione Juicio",
    df["RADICADO"].tolist(),
    key="sentencia"
)

if st.button(
    "⚖️ Registrar Sentencia"
):

    registrar_sentencia(
        radicado_sentencia
    )

    st.success(
        "Sentencia registrada correctamente"
    )

    st.rerun()