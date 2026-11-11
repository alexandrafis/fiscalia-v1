import streamlit as st

from services.auth_service import (
    validar_usuario
)

st.set_page_config(
    page_title="Fiscalía V1.0",
    layout="centered"
)

st.title(
    "🔐 Sistema Fiscalía V1.0"
)

usuario = st.text_input(
    "Usuario"
)

clave = st.text_input(
    "Contraseña",
    type="password"
)

if st.button(
    "Iniciar Sesión"
):

    resultado = validar_usuario(
        usuario,
        clave
    )

    if resultado:

        st.session_state[
            "usuario_logueado"
        ] = True

        st.session_state[
            "usuario"
        ] = resultado.usuario

        st.session_state[
            "rol"
        ] = resultado.rol

        st.success(
            f"Bienvenido {resultado.usuario}"
        )

        st.switch_page(
            "pages/00_Dashboard.py"
        )

    else:

        st.error(
            "Usuario o contraseña incorrectos"
        )