import streamlit as st

from services.correo_service import (
    enviar_correo_prueba
)

st.title(
    "📧 Prueba de Correo"
)

destinatario = st.text_input(
    "Correo Destinatario"
)

if st.button(
    "📨 Enviar Correo de Prueba"
):

    if not destinatario:

        st.error(
            "Debe ingresar un correo."
        )

    else:

        try:

            enviar_correo_prueba(
                destinatario
            )

            st.success(
                "✅ Correo enviado correctamente."
            )

        except Exception as e:

            st.error(
                f"Error al enviar correo: {e}"
            )