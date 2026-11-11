import streamlit as st

from services.delitos_service import (
    obtener_delitos
)

from services.casos_service import (
    crear_caso,
    existe_radicado
)

st.title(
    "➕ Crear Caso"
)

delitos = obtener_delitos()

if not delitos:

    st.warning(
        "No existen delitos registrados."
    )

    st.stop()

radicado = st.text_input(
    "Radicado",
    key="radicado"
)

fecha_hechos = st.date_input(
    "Fecha de Hechos",
    key="fecha_hechos"
)

delitos_dict = {
    delito.nombre: delito
    for delito in delitos
}

nombre_delito = st.selectbox(
    "Delito",
    list(delitos_dict.keys()),
    key="delito"
)

delito = delitos_dict[nombre_delito]

st.info(
    f"Pena Máxima: {delito.pena_maxima_meses} meses"
)

pena_maxima = delito.pena_maxima_meses

anios_prescripcion = max(
    5,
    int(pena_maxima / 12)
)

fecha_prescripcion = fecha_hechos.replace(
    year=fecha_hechos.year + anios_prescripcion
)

st.success(
    f"Fecha Prescripción: {fecha_prescripcion}"
)

st.info(
    """
Estado Inicial: ACTIVO

Etapa Inicial: INDAGACIÓN
"""
)

if st.button(
    "💾 Guardar Caso"
):

    if not radicado:

        st.error(
            "Debe ingresar un radicado."
        )

    elif existe_radicado(
        radicado
    ):

        st.warning(
            f"""
⚠️ El radicado {radicado}
ya existe en la base de datos.

Por favor utilice otro radicado.
"""
        )

    else:

        crear_caso(
            radicado,
            fecha_hechos,
            delito.id,
            delito.pena_maxima_meses,
            fecha_prescripcion
        )

        st.balloons()

        st.success(
            f"""
✅ CASO GUARDADO CON ÉXITO

Radicado: {radicado}

Delito: {delito.nombre}

Pena Máxima:
{delito.pena_maxima_meses} meses

Fecha Prescripción:
{fecha_prescripcion}

Etapa Inicial:
INDAGACIÓN
"""
        )
