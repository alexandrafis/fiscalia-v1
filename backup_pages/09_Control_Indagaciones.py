import streamlit as st
import pandas as pd

from datetime import date

from services.casos_service import (
    obtener_indagaciones,
    actualizar_etapa_caso
)

st.title(
    "🔍 Control de Indagaciones"
)

indagaciones = obtener_indagaciones()

if not indagaciones:

    st.warning(
        "No existen casos en INDAGACIÓN."
    )

    st.stop()

datos = []

for fila in indagaciones:

    dias_restantes = (
        fila.fecha_prescripcion -
        date.today()
    ).days

    semaforo = "🟢 VERDE"

    if dias_restantes <= 0:

        semaforo = "⚫ PRESCRITO"

    elif dias_restantes <= 180:

        semaforo = "🔴 ROJO"

    elif dias_restantes <= 365:

        semaforo = "🟠 NARANJA"

    elif dias_restantes <= 730:

        semaforo = "🟡 AMARILLO"

    datos.append(
        [
            fila.radicado,
            fila.fecha_hechos,
            fila.pena_maxima_meses,
            fila.fecha_prescripcion,
            fila.estado_caso,
            semaforo
        ]
    )

df = pd.DataFrame(
    datos,
    columns=[
        "RADICADO",
        "FECHA HECHOS",
        "PENA MAXIMA",
        "PRESCRIPCION",
        "ESTADO",
        "SEMAFORO"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

st.metric(
    "Total Indagaciones",
    len(df)
)

st.divider()

st.subheader(
    "📁 Finalizar Indagación"
)

radicado_seleccionado = st.selectbox(
    "Seleccione Caso",
    df["RADICADO"].tolist(),
    key="caso_finalizar"
)

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "📁 Archivar Caso"
    ):

        actualizar_etapa_caso(
            radicado_seleccionado,
            "ARCHIVO"
        )

        st.success(
            "Caso archivado correctamente"
        )

        st.rerun()

with col2:

    if st.button(
        "📁 Registrar Preclusión"
    ):

        actualizar_etapa_caso(
            radicado_seleccionado,
            "PRECLUSION"
        )

        st.success(
            "Preclusión registrada correctamente"
        )

        st.rerun()