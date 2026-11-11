from sqlalchemy import text

from database.connection import engine


def obtener_casos():

    sql = text(
        """
        SELECT
            id,
            radicado
        FROM casos
        ORDER BY radicado
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()

def obtener_indagaciones():

    sql = text(
        """
        SELECT

            radicado,

            fecha_hechos,

            pena_maxima_meses,

            fecha_prescripcion,

            estado_caso

        FROM casos

        WHERE etapa_actual = 'INDAGACION'

        ORDER BY fecha_prescripcion
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()

def obtener_casos_inactivos():

    sql = text(
        """
        SELECT

            radicado,

            fecha_hechos,

            fecha_prescripcion,

            etapa_actual

        FROM casos

        WHERE etapa_actual IN
        (
            'ARCHIVO',
            'PRECLUSION',
            'SENTENCIA'
        )

        ORDER BY radicado
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()

def actualizar_etapa_caso(
    radicado,
    nueva_etapa
):

    sql = text(
        """
        UPDATE casos
        SET etapa_actual = :nueva_etapa
        WHERE radicado = :radicado
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "radicado": radicado,
                "nueva_etapa": nueva_etapa
            }
        )

def registrar_sentencia(
    radicado
):

    sql = text(
        """
        UPDATE casos
        SET etapa_actual = 'SENTENCIA'
        WHERE radicado = :radicado
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "radicado": radicado
            }
        )

def existe_radicado(
    radicado
):

    sql = text(
        """
        SELECT COUNT(*)
        FROM casos
        WHERE radicado = :radicado
        """
    )

    with engine.connect() as conn:

        cantidad = conn.execute(
            sql,
            {
                "radicado": radicado
            }
        ).scalar()

        return cantidad > 0

from datetime import timedelta

def crear_caso(
    radicado,
    fecha_hechos,
    delito_id,
    pena_maxima_meses,
    fecha_prescripcion
):

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
            etapa_actual
        )
        VALUES
        (
            :radicado,
            :fecha_hechos,
            :delito_id,
            :pena_maxima_meses,
            :fecha_prescripcion,
            'ACTIVO',
            'INDAGACION'
        )
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "radicado": radicado,
                "fecha_hechos": fecha_hechos,
                "delito_id": delito_id,
                "pena_maxima_meses": pena_maxima_meses,
                "fecha_prescripcion": fecha_prescripcion
            }
        )

def existe_radicado(
    radicado
):

    sql = text(
        """
        SELECT COUNT(*)
        FROM casos
        WHERE radicado = :radicado
        """
    )

    with engine.connect() as conn:

        cantidad = conn.execute(
            sql,
            {
                "radicado": radicado
            }
        ).scalar()

        return cantidad > 0        