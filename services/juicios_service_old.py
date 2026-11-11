from sqlalchemy import text
from database.connection import engine


def guardar_datos_juicio(
    radicado,
    fecha_imputacion,
    fecha_acusacion,
    etapa_procesal,
    fecha_prescripcion_juicio
):

    sql = text("""
        UPDATE casos
        SET
            fecha_imputacion = :fecha_imputacion,
            fecha_acusacion = :fecha_acusacion,
            etapa_procesal = :etapa_procesal,
            fecha_prescripcion_juicio = :fecha_prescripcion_juicio
        WHERE radicado = :radicado
    """)

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "radicado": radicado,
                "fecha_imputacion": fecha_imputacion,
                "fecha_acusacion": fecha_acusacion,
                "etapa_procesal": etapa_procesal,
                "fecha_prescripcion_juicio": fecha_prescripcion_juicio
            }
        )


def obtener_datos_caso_juicio(radicado):

    sql = text("""
        SELECT
            radicado,
            pena_maxima_meses,
            fecha_prescripcion
        FROM casos
        WHERE radicado = :radicado
    """)

    with engine.connect() as conn:

        resultado = conn.execute(
            sql,
            {
                "radicado": radicado
            }
        )

        return resultado.fetchone()
