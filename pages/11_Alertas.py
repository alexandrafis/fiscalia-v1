import pandas as pd

from io import BytesIO

import streamlit as st

from sqlalchemy import text

from database.connection import engine
from services.alertas import (
    calcular_dias_restantes,
    calcular_semaforo
)

st.title(
    "🚨 Alertas de Prescripción"
)

buscar_radicado = st.text_input(
    "🔎 Buscar por Radicado"
)

filtro = st.selectbox(
    "Filtrar por semáforo",
    [
        "TODOS",
        "VERDE",
        "AMARILLO",
        "NARANJA",
        "ROJO",
        "NEGRO"
    ]
)

consulta = text(
    """
    SELECT
        radicado,
        fecha_hechos,
        fecha_prescripcion
    FROM casos
    """
)

with engine.connect() as conn:

    resultados = conn.execute(
        consulta
    )

    datos = []

    for fila in resultados:

        dias = calcular_dias_restantes(
            fila.fecha_prescripcion
        )

        semaforo = calcular_semaforo(
            dias
        )

        datos.append(
            {
                "RADICADO": fila.radicado,
                "FECHA_HECHOS": fila.fecha_hechos,
                "FECHA_PRESCRIPCION":
                    fila.fecha_prescripcion,
                "DIAS_RESTANTES": dias,
                "SEMAFORO": semaforo
            }
        )

df = pd.DataFrame(datos)

if filtro != "TODOS":

    df = df[
        df["SEMAFORO"] == filtro
    ]

if buscar_radicado:

    df = df[
        df["RADICADO"]
        .astype(str)
        .str.contains(
            buscar_radicado,
            case=False,
            na=False
        )
    ]

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False,
        sheet_name="Alertas"
    )

excel_buffer.seek(0)

st.download_button(
    label="📥 Exportar Alertas a Excel",
    data=excel_buffer,
    file_name="alertas_prescripcion.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)