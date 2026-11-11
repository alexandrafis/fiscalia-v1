from services.casos_service import (
    obtener_casos
)

from services.ordenes_service import (
    guardar_orden,
    obtener_ordenes,
    eliminar_orden,
    actualizar_estado_orden,
    actualizar_orden
    )

import streamlit as st

st.title("📑 Órdenes Policía Judicial")

st.write("Módulo de Órdenes PJ funcionando")

numero_orden = st.text_input(
    "Número Orden"
)

casos = obtener_casos()

casos_dict = {
    fila.radicado: fila.id
    for fila in casos
}

radicado_seleccionado = st.selectbox(
    "Caso",
    list(casos_dict.keys())
)

caso_id = casos_dict[
    radicado_seleccionado
]

tipo = st.selectbox(
    "Tipo Orden",
    [
        "ENTREVISTA",
        "INSPECCION",
        "BUSQUEDA_SELECTIVA",
        "ANALISIS_FORENSE",
        "OTRA"
    ]
)

fecha_inicio = st.date_input(
    "Fecha Inicio"
)

termino = st.number_input(
    "Término (días)",
    min_value=1,
    value=30
)

from datetime import timedelta

fecha_vencimiento = (
    fecha_inicio +
    timedelta(days=termino)
)

st.info(
    f"Fecha Vencimiento: {fecha_vencimiento}"
)

from datetime import date

dias_restantes = (
    fecha_vencimiento -
    date.today()
).days

if dias_restantes <= 0:

    st.error(
        f"⚫ VENCIDA ({dias_restantes} días)"
    )

elif dias_restantes <= 5:

    st.error(
        f"🔴 CRÍTICA ({dias_restantes} días)"
    )

elif dias_restantes <= 10:

    st.warning(
        f"🟠 NARANJA ({dias_restantes} días)"
    )

elif dias_restantes <= 15:

    st.warning(
        f"🟡 AMARILLA ({dias_restantes} días)"
    )

else:

    st.success(
        f"🟢 VERDE ({dias_restantes} días)"
    )

semaforo = "VERDE"

if dias_restantes <= 0:
    semaforo = "NEGRO"

elif dias_restantes <= 5:
    semaforo = "ROJO"

elif dias_restantes <= 10:
    semaforo = "NARANJA"

elif dias_restantes <= 15:
    semaforo = "AMARILLO"

if st.button(
    "Guardar Orden"
):

    try:

        guardar_orden(
            caso_id,
            numero_orden,
            tipo,
            fecha_inicio,
            termino,
            fecha_vencimiento,
            "ACTIVA",
            semaforo
        )

        st.success(
            "Orden registrada correctamente"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

st.subheader(
    "📋 Órdenes Registradas"
)

import pandas as pd

ordenes = obtener_ordenes()

if ordenes:

    df = pd.DataFrame(
        ordenes,
        columns=[
            "ORDEN",
            "CASO",
            "TIPO",
            "VENCIMIENTO",
            "ESTADO",
            "SEMAFORO"
        ]
    )

    filtro_estado = st.selectbox(
        "Filtrar Estado",
        [
            "TODAS",
            "ACTIVA",
            "CUMPLIDA"
        ]
    )

    if filtro_estado == "ACTIVA":

        df = df[
            df["ESTADO"]
            .fillna("")
            .astype(str)
            .str.upper()
            == "ACTIVA"
        ]

    elif filtro_estado == "CUMPLIDA":

        df = df[
            df["ESTADO"]
            .fillna("")
            .astype(str)
            .str.upper()
            == "CUMPLIDA"
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "⚙ Gestión de Órdenes"
    )

    if not df.empty:

        orden_seleccionada = st.selectbox(
            "Seleccione Orden",
            df["ORDEN"].tolist()
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🗑 Eliminar Orden"
            ):

                eliminar_orden(
                    orden_seleccionada
                )

                st.success(
                    "Orden eliminada correctamente"
                )

                st.rerun()

        with col2:

            if st.button(
                "✅ Marcar Cumplida"
            ):

                actualizar_estado_orden(
                    orden_seleccionada,
                    "CUMPLIDA"
                )

                st.success(
                    "Orden actualizada correctamente"
                )

                st.rerun()

st.divider()

from datetime import date, timedelta

st.divider()

st.subheader(
    "✏️ Editar Orden"
)

orden_editar = st.selectbox(
    "Seleccione Orden a Editar",
    df["ORDEN"].dropna().tolist(),
    key="editar_orden"
)

nuevo_tipo = st.selectbox(
    "Nuevo Tipo",
    [
        "ENTREVISTA",
        "INSPECCION",
        "BUSQUEDA_SELECTIVA",
        "ANALISIS_FORENSE",
        "OTRA"
    ]
)

nueva_fecha_inicio = st.date_input(
    "Nueva Fecha Inicio"
)

nuevo_termino = st.number_input(
    "Nuevo Término (días)",
    min_value=1,
    value=30
)

nuevo_estado = st.selectbox(
    "Nuevo Estado",
    [
        "ACTIVA",
        "CUMPLIDA"
    ]
)

nueva_fecha_vencimiento = (
    nueva_fecha_inicio +
    timedelta(days=nuevo_termino)
)

st.info(
    f"Nuevo vencimiento: {nueva_fecha_vencimiento}"
)

dias_restantes = (
    nueva_fecha_vencimiento -
    date.today()
).days

semaforo = "VERDE"

if dias_restantes <= 0:
    semaforo = "NEGRO"

elif dias_restantes <= 5:
    semaforo = "ROJO"

elif dias_restantes <= 10:
    semaforo = "NARANJA"

elif dias_restantes <= 15:
    semaforo = "AMARILLO"

st.write(
    f"Semáforo calculado: {semaforo}"
)

if st.button(
    "💾 Guardar Cambios"
):

    actualizar_orden(
        orden_editar,
        nuevo_tipo,
        nueva_fecha_inicio,
        nuevo_termino,
        nueva_fecha_vencimiento,
        nuevo_estado,
        semaforo
    )

    st.success(
        "Orden actualizada correctamente"
    )

    st.rerun()