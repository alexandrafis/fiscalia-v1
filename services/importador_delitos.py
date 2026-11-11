from sqlalchemy import text

from database.connection import engine


def guardar_delitos(df):

    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    insertados = 0

    with engine.begin() as conn:

        for _, fila in df.iterrows():

            conn.execute(
                text(
                    """
                    INSERT INTO delitos
                    (
                        codigo,
                        nombre,
                        pena_maxima_meses
                    )
                    VALUES
                    (
                        :codigo,
                        :nombre,
                        :pena
                    )
                    """
                ),
                {
                    "codigo": f"D{insertados+1:03}",
                    "nombre": str(
                        fila["DELITO"]
                    ).strip(),
                    "pena": int(
                        fila["PENA MAXIMA EN MESES"]
                    )
                }
            )

            insertados += 1

    return insertados