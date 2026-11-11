from sqlalchemy import text

from database.connection import engine


def obtener_configuracion():

    sql = text(
        """
        SELECT *
        FROM configuracion_alertas
        LIMIT 1
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchone()


def guardar_configuracion(
    correo_destino,

    indagacion_1,
    indagacion_2,
    indagacion_3,
    indagacion_4,

    juicio_1,
    juicio_2,
    juicio_3,
    juicio_4,

    alerta_orden_1,
    alerta_orden_2,
    alerta_orden_3,
    alerta_orden_4
):

    sql = text(
        """
        UPDATE configuracion_alertas
        SET

            correo_destino = :correo_destino,

            indagacion_1 = :indagacion_1,
            indagacion_2 = :indagacion_2,
            indagacion_3 = :indagacion_3,
            indagacion_4 = :indagacion_4,

            juicio_1 = :juicio_1,
            juicio_2 = :juicio_2,
            juicio_3 = :juicio_3,
            juicio_4 = :juicio_4,

            alerta_orden_1 = :alerta_orden_1,
            alerta_orden_2 = :alerta_orden_2,
            alerta_orden_3 = :alerta_orden_3,
            alerta_orden_4 = :alerta_orden_4

        WHERE id = 1
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "correo_destino": correo_destino,

                "indagacion_1": indagacion_1,
                "indagacion_2": indagacion_2,
                "indagacion_3": indagacion_3,
                "indagacion_4": indagacion_4,

                "juicio_1": juicio_1,
                "juicio_2": juicio_2,
                "juicio_3": juicio_3,
                "juicio_4": juicio_4,

                "alerta_orden_1": alerta_orden_1,
                "alerta_orden_2": alerta_orden_2,
                "alerta_orden_3": alerta_orden_3,
                "alerta_orden_4": alerta_orden_4
            }
        )