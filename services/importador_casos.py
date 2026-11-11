import pandas as pd

from sqlalchemy import text

from database.connection import engine

from services.delitos_service import (
    buscar_delito_por_nombre
)

from services.prescripcion import (
    calcular_prescripcion_indagacion
)

def guardar_casos(df):

    insertados = 0

    with engine.begin() as conn:

        for _, fila in df.iterrows():

            sql = text(
                """
                INSERT INTO casos
                (
                    radicado,
                    fecha_hechos,
                    delito_id,
                    pena_maxima_meses,
                    fecha_prescripcion,
                    estado_caso,
                    etapa_actual,
                    etapa_procesal
                )
                VALUES
                (
                    :radicado,
                    :fecha_hechos,
                    :delito_id,
                    :pena_maxima_meses,
                    :fecha_prescripcion,
                    :estado_caso,
                    :etapa_actual,
                    :etapa_procesal
                )
                """
            )

            nombre_delito = str(
                fila["DELITO"]
            ).strip()

            delito = buscar_delito_por_nombre(
                nombre_delito
            )
            print("BUSCANDO:", nombre_delito)
            print("RESULTADO:", delito)

            if not delito:

                continue

            fecha_hechos = pd.to_datetime(
                fila["FECHA_HECHOS"]
            )

            fecha_prescripcion = (
                calcular_prescripcion_indagacion(
                    fecha_hechos,
                    delito.pena_maxima_meses
                )
            )

            etapa = str(
                fila["ETAPA"]
            ).strip().upper()

            if etapa == "JUICIO":

                etapa_final = "JUICIO"

            else:

                etapa_final = "INDAGACION"

            conn.execute(
                sql,
                {
                    "radicado": str(
                        fila["RADICADO"]
                    ),

                    "fecha_hechos": fila[
                        "FECHA_HECHOS"
                    ],

                    "delito_id": delito.id,

                    "pena_maxima_meses": delito.pena_maxima_meses,

                    "fecha_prescripcion": fecha_prescripcion,

                    "estado_caso": "ACTIVO",

                    "etapa_actual": etapa_final,

                    "etapa_procesal": etapa
                }
            )

            insertados += 1

    return insertados