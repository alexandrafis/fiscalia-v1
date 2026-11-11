from sqlalchemy import text

from database.connection import engine


def guardar_destinatario(
    nombre,
    correo,
    cargo,
    alerta_indagacion,
    alerta_juicio,
    alerta_orden_pj,
    activo
):

    sql = text(
        """
        INSERT INTO destinatarios_alertas
        (
            nombre,
            correo,
            cargo,
            alerta_indagacion,
            alerta_juicio,
            alerta_orden_pj,
            activo
        )
        VALUES
        (
            :nombre,
            :correo,
            :cargo,
            :alerta_indagacion,
            :alerta_juicio,
            :alerta_orden_pj,
            :activo
        )
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "nombre": nombre,
                "correo": correo,
                "cargo": cargo,
                "alerta_indagacion": alerta_indagacion,
                "alerta_juicio": alerta_juicio,
                "alerta_orden_pj": alerta_orden_pj,
                "activo": activo
            }
        )


def obtener_destinatarios():

    sql = text(
        """
        SELECT
            id,
            nombre,
            correo,
            alerta_indagacion,
            alerta_juicio,
            alerta_orden_pj,
            activo
        FROM destinatarios_alertas
        ORDER BY nombre
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()

def existe_correo(
    correo
):

    sql = text(
        """
        SELECT COUNT(*)
        FROM destinatarios_alertas
        WHERE UPPER(correo) = UPPER(:correo)
        """
    )

    with engine.connect() as conn:

        cantidad = conn.execute(
            sql,
            {
                "correo": correo
            }
        ).scalar()

        return cantidad > 0

def existe_correo(
    correo
):

    sql = text(
        """
        SELECT COUNT(*)
        FROM destinatarios_alertas
        WHERE UPPER(correo) = UPPER(:correo)
        """
    )

    with engine.connect() as conn:

        cantidad = conn.execute(
            sql,
            {
                "correo": correo
            }
        ).scalar()

        return cantidad > 0

from sqlalchemy import text


def obtener_destinatarios_indagacion():

    sql = text(
        """
        SELECT
            correo
        FROM destinatarios_alertas
        WHERE activo = TRUE
        AND alerta_indagacion = TRUE
        """
    )

    with engine.connect() as conn:

        return conn.execute(
            sql
        ).fetchall()

def obtener_destinatarios_juicio():

    sql = text(
        """
        SELECT
            correo
        FROM destinatarios_alertas
        WHERE activo = TRUE
        AND alerta_juicio = TRUE
        """
    )

    with engine.connect() as conn:

        return conn.execute(
            sql
        ).fetchall()

def obtener_destinatarios_orden_pj():

    sql = text(
        """
        SELECT
            correo
        FROM destinatarios_alertas
        WHERE activo = TRUE
        AND alerta_orden_pj = TRUE
        """
    )

    with engine.connect() as conn:

        return conn.execute(
            sql
        ).fetchall()