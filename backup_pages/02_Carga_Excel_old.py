import streamlit as st
import pandas as pd

from services.importador_casos import guardar_casos

st.title("📂 Carga Masiva de Casos")

archivo = st.file_uploader(
    "Seleccione archivo Excel",
    type=["xlsx", "xls"]
)

if archivo:

    df = pd.read_excel(archivo)

    st.success(
        f"Archivo cargado correctamente ({len(df)} registros)"
    )

    st.subheader("Vista previa")

    df_editado = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    st.subheader("Columnas encontradas")

    st.write(list(df.columns))

    if st.button("Guardar en PostgreSQL"):

        try:

            cantidad = guardar_casos(
                df_editado
            )

            st.success(
                f"✅ {cantidad} registros guardados correctamente"
            )

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )