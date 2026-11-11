import streamlit as st
import pandas as pd

from services.destinatarios_alertas_service import (
    guardar_destinatario,
    obtener_destinatarios,
    existe_correo
)

st.title(
    "📧 Destinatarios de Alertas"
)

st.subheader(
    "➕ Nuevo Destinatario"
)

nombre = st.text_input(
    "Nombre"
)

correo = st.text_input(
    "Correo Electrónico"
)

cargo = st.text_input(
    "Cargo / Dependencia"
)

alerta_indagacion = st.checkbox(
    "🔍 Recibe alertas de Indagación",
    value=True
)

alerta_juicio = st.checkbox(
    "⚖️ Recibe alertas de Juicio",
    value=True
)

alerta_orden_pj = st.checkbox(
    "📋 Recibe alertas de Órdenes PJ",
    value=True
)

activo = st.checkbox(
    "✅ Destinatario Activo",
    value=True
)

if st.button(
    "💾 Guardar Destinatario"
):

    if not nombre:

        st.error(
            "Debe ingresar un nombre."
        )

    elif not correo:

        st.error(
            "Debe ingresar un correo."
        )

    elif not cargo:

        st.error(
            "Debe ingresar un cargo o dependencia."
        )

    elif existe_correo(correo):

        st.warning(
            f"⚠️ El correo {correo} ya se encuentra registrado."
        )

    else:

        guardar_destinatario(
            nombre,
            correo,
            cargo,
            alerta_indagacion,
            alerta_juicio,
            alerta_orden_pj,
            activo
        )

        st.success(
            "✅ Destinatario guardado correctamente."
        )

st.divider()

st.subheader(
    "📋 Destinatarios Registrados"
)

destinatarios = obtener_destinatarios()

if destinatarios:

    df = pd.DataFrame(
        destinatarios,
        columns=[
            "ID",
            "NOMBRE",
            "CORREO",
            "INDAGACION",
            "JUICIO",
            "ORDEN_PJ",
            "ACTIVO"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No existen destinatarios registrados."
    )