import streamlit as st
import pandas as pd

from datetime import date

from sqlalchemy import text

from database.connection import engine

from services.historial_alertas_service import (
    contar_alertas_pendientes,
    contar_alertas_enviadas,
    contar_alertas_error,
    contar_alertas_criticas
)

st.title(
    "📊 Dashboard Jurídico"
)

# --------------------------------
# KPI PRINCIPALES
# --------------------------------

sql_indagacion = text(
    """
    SELECT COUNT(*)
    FROM casos
    WHERE etapa_actual = 'INDAGACION'
    """
)

sql_juicios = text(
    """
    SELECT COUNT(*)
    FROM casos
    WHERE etapa_actual = 'JUICIO'
    """
)

sql_inactivos = text(
    """
    SELECT COUNT(*)
    FROM casos
    WHERE etapa_actual IN
    (
        'ARCHIVO',
        'PRECLUSION',
        'SENTENCIA'
    )
    """
)

sql_ordenes = text(
    """
    SELECT COUNT(*)
    FROM ordenes_pj
    WHERE estado = 'ACTIVA'
    """
)

with engine.connect() as conn:

    total_indagacion = conn.execute(
        sql_indagacion
    ).scalar()

    total_juicios = conn.execute(
        sql_juicios
    ).scalar()

    total_inactivos = conn.execute(
        sql_inactivos
    ).scalar()

    total_ordenes = conn.execute(
        sql_ordenes
    ).scalar()

alertas_pendientes = (
    contar_alertas_pendientes()
)

alertas_enviadas = (
    contar_alertas_enviadas()
)

alertas_error = (
    contar_alertas_error()
)

alertas_criticas = (
    contar_alertas_criticas()
)    

sql_etapas = text(
    """
    SELECT
        etapa_actual,
        COUNT(*) AS cantidad
    FROM casos
    GROUP BY etapa_actual
    ORDER BY etapa_actual
    """
)

with engine.connect() as conn:

    etapas = conn.execute(
        sql_etapas
    ).fetchall()

df_etapas = pd.DataFrame(
    etapas,
    columns=[
        "ETAPA",
        "CANTIDAD"
    ]
)

sql_ordenes_estado = text(
    """
    SELECT
        estado,
        COUNT(*) AS cantidad
    FROM ordenes_pj
    GROUP BY estado
    ORDER BY estado
    """
)

with engine.connect() as conn:

    ordenes_estado = conn.execute(
        sql_ordenes_estado
    ).fetchall()

df_ordenes = pd.DataFrame(
    ordenes_estado,
    columns=[
        "ESTADO",
        "CANTIDAD"
    ]
)    

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "🔍 Indagaciones",
        total_indagacion
    )

with col2:

    st.metric(
        "⚖️ Juicios",
        total_juicios
    )

col3, col4 = st.columns(2)

with col3:

    st.metric(
        "📁 Inactivos",
        total_inactivos
    )

with col4:

    st.metric(
        "📋 Órdenes PJ Activas",
        total_ordenes
    )

st.subheader(
    "🚨 Estado de Alertas"
)

col5, col6, col7, col8 = st.columns(4)

with col5:

    st.metric(
        "🟡 Pendientes",
        alertas_pendientes
    )

with col6:

    st.metric(
        "🟢 Enviadas",
        alertas_enviadas
    )

with col7:

    st.metric(
        "🔴 Error",
        alertas_error
    )

with col8:

    st.metric(
        "⚠️ Críticas",
        alertas_criticas
    )    

# --------------------------------
# RESUMEN
# --------------------------------

st.divider()

st.subheader(
    "📌 Resumen General"
)

st.write(
    f"""
🔍 Indagaciones activas: {total_indagacion}

⚖️ Juicios activos: {total_juicios}

📁 Procesos finalizados: {total_inactivos}

📋 Órdenes PJ activas: {total_ordenes}
"""
)

# --------------------------------
# ALERTAS CRÍTICAS
# --------------------------------

st.divider()

st.subheader(
    "🚨 Alertas Críticas"
)

sql_alerta_indagacion = text(
    """
    SELECT COUNT(*)
    FROM casos
    WHERE etapa_actual = 'INDAGACION'
    AND fecha_prescripcion <= CURRENT_DATE + INTERVAL '365 days'
    """
)

with engine.connect() as conn:

    alerta_indagacion = conn.execute(
        sql_alerta_indagacion
    ).scalar()

st.error(
    f"🔍 Indagaciones próximas a prescribir: {alerta_indagacion}"
)

sql_alerta_juicio = text(
    """
    SELECT COUNT(*)
    FROM juicios
    WHERE fecha_prescripcion_juicio <=
    CURRENT_DATE + INTERVAL '180 days'
    """
)

with engine.connect() as conn:

    alerta_juicio = conn.execute(
        sql_alerta_juicio
    ).scalar()

st.error(
    f"⚖️ Juicios próximos a prescribir: {alerta_juicio}"
)

sql_alerta_orden = text(
    """
    SELECT COUNT(*)
    FROM ordenes_pj
    WHERE estado = 'ACTIVA'
    AND fecha_vencimiento <=
        CURRENT_DATE + INTERVAL '30 days'
    """
)

with engine.connect() as conn:

    alerta_orden = conn.execute(
        sql_alerta_orden
    ).scalar()

st.error(
    f"📋 Órdenes PJ próximas a vencer: {alerta_orden}"
)

st.warning(
    f"""
    🔍 Indagaciones activas: {total_indagacion}

    ⚖️ Juicios activos: {total_juicios}

    📋 Órdenes PJ activas: {total_ordenes}

    Revise periódicamente los módulos de control
    para verificar prescripciones y vencimientos.
    """
)

st.divider()

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "📊 Casos por Etapa"
    )

    st.bar_chart(
        df_etapas.set_index(
            "ETAPA"
        )
    )

with col2:

    st.subheader(
        "📋 Órdenes PJ por Estado"
    )

    st.bar_chart(
        df_ordenes.set_index(
            "ESTADO"
        )
    )

st.divider()

st.subheader(
    "🚨 Detalle de Alertas"
)

sql_detalle_alertas = text(
    """
    SELECT
        radicado,
        etapa_actual,
        fecha_prescripcion AS fecha_alerta
    FROM casos
    WHERE
    (
        etapa_actual = 'INDAGACION'
        AND fecha_prescripcion <=
            CURRENT_DATE + INTERVAL '365 days'
    )

    UNION

    SELECT
        c.radicado,
        c.etapa_actual,
        j.fecha_prescripcion_juicio AS fecha_alerta
    FROM juicios j

    INNER JOIN casos c
        ON c.id = j.caso_id

    WHERE
        c.etapa_actual = 'JUICIO'
        AND j.fecha_prescripcion_juicio <=
            CURRENT_DATE + INTERVAL '180 days'

    UNION

    SELECT
        numero_orden,
        'ORDEN_PJ',
        fecha_vencimiento
    FROM ordenes_pj

    WHERE
        estado = 'ACTIVA'
        AND fecha_vencimiento <=
            CURRENT_DATE + INTERVAL '30 days'

    ORDER BY fecha_alerta
    """
)

with engine.connect() as conn:

    alertas = conn.execute(
        sql_detalle_alertas
    ).fetchall()

if alertas:

    df_alertas = pd.DataFrame(
        alertas,
        columns=[
            "IDENTIFICADOR",
            "TIPO",
            "FECHA_ALERTA"
        ]
    )

    df_alertas["FECHA_ALERTA"] = pd.to_datetime(
        df_alertas["FECHA_ALERTA"],
        errors="coerce"
)

    df_alertas["DIAS_RESTANTES"] = (
        df_alertas["FECHA_ALERTA"]
        - pd.Timestamp.today()
    ).dt.days    

    st.dataframe(
        df_alertas,
        use_container_width=True
    )

else:

    st.success(
        "✅ No existen alertas de prescripción."
    )