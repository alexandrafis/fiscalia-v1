import streamlit as st

def verificar_sesion():

    if not st.session_state.get(
        "usuario_logueado",
        False
    ):

        st.warning(
            "Debe iniciar sesión."
        )

        st.stop()