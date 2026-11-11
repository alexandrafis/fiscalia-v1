from sqlalchemy import text

from database.connection import engine


def obtener_casos_indagacion():

    sql = text(
        """
        SELECT
            id,
            radicado,
            pena_maxima_meses,
            etapa_actual
        FROM casos
        WHERE etapa_actual = 'INDAGACION'
        ORDER BY radicado
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()


def trasladar_a_juicio(
    caso_id,
    tipo_actuacion,
    fecha_actuacion,
    fecha_prescripcion_juicio
):

    with engine.begin() as conn:

        sql_caso = text(
            """
            UPDATE casos
            SET etapa_actual = 'JUICIO'
            WHERE id = :caso_id
            """
        )

        conn.execute(
            sql_caso,
            {
                "caso_id": caso_id
            }
        )

        fecha_imputacion = None
        fecha_acusacion = None
        fecha_traslado = None

        if tipo_actuacion == "IMPUTACION":
            fecha_imputacion = fecha_actuacion

        if tipo_actuacion == "ACUSACION":
            fecha_acusacion = fecha_actuacion
            fecha_traslado = fecha_actuacion

        sql_juicio = text(
            """
            INSERT INTO juicios
            (
                caso_id,
                tipo_actuacion,
                fecha_imputacion,
                fecha_acusacion,
                fecha_traslado,
                fecha_inicio_prescripcion,
                etapa_procesal,
                fecha_prescripcion_juicio,
                estado_juicio
            )
            VALUES
            (
                :caso_id,
                :tipo_actuacion,
                :fecha_imputacion,
                :fecha_acusacion,
                :fecha_traslado,
                :fecha_inicio_prescripcion,
                'JUICIO',
                :fecha_prescripcion_juicio,
                'ACTIVO'
            )
            """
        )

        conn.execute(
            sql_juicio,
            {
                "caso_id": caso_id,
                "tipo_actuacion": tipo_actuacion,
                "fecha_imputacion": fecha_imputacion,
                "fecha_acusacion": fecha_acusacion,
                "fecha_traslado": fecha_traslado,
                "fecha_inicio_prescripcion": fecha_actuacion,
                "fecha_prescripcion_juicio": fecha_prescripcion_juicio
            }
        )

def obtener_juicios():

    sql = text(
        """
        SELECT

            radicado,

            etapa_procesal AS tipo_actuacion,

            fecha_acusacion AS fecha_inicio_prescripcion,

            fecha_prescripcion_juicio,

            estado_caso AS estado_juicio

        FROM casos

        WHERE etapa_actual = 'JUICIO'

        ORDER BY radicado
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        filas = resultado.fetchall()

        print("TOTAL JUICIOS:", len(filas))

        return filas

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