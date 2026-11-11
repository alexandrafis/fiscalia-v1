import streamlit as st
import pandas as pd

from services.historial_alertas_service import (
    obtener_historial
)

st.title(
    "📜 Historial de Alertas"
)

historial = obtener_historial()

if historial:

    df = pd.DataFrame(
        historial,
        columns=[
            "ID",
            "FECHA",
            "TIPO_ALERTA",
            "RADICADO",
            "ETAPA",
            "DIAS_RESTANTES",
            "DESTINATARIO",
            "ASUNTO",
            "ESTADO",
            "ENVIADO"
        ]
    )

    pendientes = len(
        df[df["ESTADO"] == "PENDIENTE"]
    )

    enviadas = len(
        df[df["ESTADO"] == "ENVIADA"]
    )

    errores = len(
        df[df["ESTADO"] == "ERROR"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🟡 Pendientes",
            pendientes
        )

    with col2:
        st.metric(
            "🟢 Enviadas",
            enviadas
        )

    with col3:
        st.metric(
            "🔴 Error",
            errores
        )

    st.dataframe(
        df,
        width="stretch"
    )

else:

    st.info(
        "No existen alertas registradas."
    )