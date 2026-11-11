import pandas as pd
import streamlit as st

from services.casos_service import (
    obtener_casos
)

from services.consulta_service import (
    obtener_detalle_caso,
    obtener_ordenes_caso
)

st.title(
    "📂 Consulta Integral del Caso"
)

casos = obtener_casos()

radicados = [
    fila.radicado
    for fila in casos
]

radicado = st.selectbox(
    "Seleccione Caso",
    radicados
)

detalle = obtener_detalle_caso(
    radicado
)

if detalle:

    st.subheader(
        "📋 Información General"
    )

    st.write(
        f"**Radicado:** {detalle.radicado}"
    )

    st.write(
        f"**Delito:** {detalle.delito}"
    )

    st.write(
        f"**Fecha Hechos:** {detalle.fecha_hechos}"
    )

    st.write(
        f"**Pena Máxima:** "
        f"{detalle.pena_maxima_meses} meses"
    )

    st.write(
        f"**Fecha Prescripción:** "
        f"{detalle.fecha_prescripcion}"
    )

    st.divider()

    st.subheader(
        "📑 Órdenes PJ Asociadas"
    )

    ordenes = obtener_ordenes_caso(
        detalle.id
    )

    if ordenes:

        df = pd.DataFrame(
            ordenes,
            columns=[
                "ORDEN",
                "TIPO",
                "VENCIMIENTO",
                "SEMAFORO"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No existen órdenes asociadas."
        )