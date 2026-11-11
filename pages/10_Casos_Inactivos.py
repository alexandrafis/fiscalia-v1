import streamlit as st

import pandas as pd

from services.casos_service import (
    obtener_casos_inactivos
)

st.title(
    "📁 Casos Inactivos"
)

casos = obtener_casos_inactivos()

if not casos:

    st.warning(
        "No existen casos inactivos registrados."
    )

    st.stop()

datos = []

for fila in casos:

    datos.append(
        [
            fila.radicado,
            fila.fecha_hechos,
            fila.fecha_prescripcion,
            fila.etapa_actual
        ]
    )

df = pd.DataFrame(
    datos,
    columns=[
        "RADICADO",
        "FECHA HECHOS",
        "PRESCRIPCION",
        "ESTADO FINAL"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

st.metric(
    "Total Casos Inactivos",
    len(df)
)