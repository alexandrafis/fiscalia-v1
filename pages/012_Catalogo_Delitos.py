import streamlit as st

from services.delitos_service import (
    guardar_delito,
    obtener_delitos
)

import pandas as pd

from services.importador_delitos import (
    guardar_delitos
)

st.title("📚 Catálogo de Delitos")

tab1, tab2 = st.tabs(
    [
        "➕ Crear Delito",
        "📂 Carga Masiva"
    ]
)

with tab1:

    codigo = st.text_input(
    "Código"
    )

    nombre = st.text_input(
    "Nombre Delito"
    )

    pena = st.number_input(
    "Pena Máxima (Meses)",
    min_value=1
    )

    if st.button(
        "Guardar Delito"
    ):

        try:

            guardar_delito(
                codigo,
                nombre,
                pena
            )

            st.success(
                "Delito guardado correctamente"
            )

        except Exception as e:

            st.error(str(e))
    st.divider()

with tab2:

    archivo = st.file_uploader(
        "Seleccione archivo Excel de delitos",
        type=["xlsx", "xls"]
    )

    if archivo:

        df = pd.read_excel(
            archivo
        )

        df.columns = df.columns.str.strip()

        st.write("COLUMNAS LIMPIAS")
        st.write(df.columns.tolist())

        st.dataframe(
            df,
            use_container_width=True
        )

        if st.button(
            "📂 Cargar Delitos"
        ):

            try:

                cantidad = guardar_delitos(
                    df
                )

                st.success(
                    f"✅ {cantidad} delitos cargados correctamente"
                )

            except Exception as e:

                st.error(
                    repr(e)
                )

st.subheader(
    "📋 Delitos Registrados"
)

delitos = obtener_delitos()

if delitos:

    import pandas as pd

    df = pd.DataFrame(
        delitos,
        columns=[
            "ID",
            "CODIGO",
            "NOMBRE",
            "PENA_MAXIMA_MESES"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No existen delitos registrados."
    )

