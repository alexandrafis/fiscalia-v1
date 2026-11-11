from sqlalchemy import text

from database.connection import engine


def obtener_detalle_caso(
    radicado
):

    sql = text(
        """
        SELECT
            c.id,
            c.radicado,
            c.fecha_hechos,
            c.fecha_prescripcion,
            c.pena_maxima_meses,
            d.nombre as delito
        FROM casos c
        LEFT JOIN delitos d
            ON c.delito_id = d.id
        WHERE c.radicado = :radicado
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(
            sql,
            {
                "radicado": radicado
            }
        )

        return resultado.fetchone()


def obtener_ordenes_caso(
    caso_id
):

    sql = text(
        """
        SELECT
            numero_orden,
            tipo_orden,
            fecha_vencimiento,
            semaforo
        FROM ordenes_pj
        WHERE caso_id = :caso_id
        ORDER BY fecha_vencimiento
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(
            sql,
            {
                "caso_id": caso_id
            }
        )

        return resultado.fetchall()