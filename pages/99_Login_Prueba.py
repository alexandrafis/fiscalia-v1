import streamlit as st

from services.auth_service import (
    validar_usuario
)

st.title(
    "🔐 Acceso al Sistema"
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

        st.success(
            f"Bienvenido {resultado.usuario}"
        )

        st.info(
            f"Rol: {resultado.rol}"
        )

    else:

        st.error(
            "Usuario o contraseña incorrectos"
        )