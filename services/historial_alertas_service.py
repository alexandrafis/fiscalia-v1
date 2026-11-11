from sqlalchemy import text

from database.connection import engine


def registrar_alerta(
    tipo_alerta,
    destinatario,
    asunto,
    mensaje,
    radicado=None,
    dias_restantes=None,
    etapa=None,
    enviado=False,
    estado="PENDIENTE"
):

    sql = text(
        """
        INSERT INTO historial_alertas
        (
            tipo_alerta,
            destinatario,
            asunto,
            mensaje,
            radicado,
            dias_restantes,
            etapa,
            enviado,
            estado
        )
        VALUES
        (
            :tipo_alerta,
            :destinatario,
            :asunto,
            :mensaje,
            :radicado,
            :dias_restantes,
            :etapa,
            :enviado,
            :estado
        )
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "tipo_alerta": tipo_alerta,
                "destinatario": destinatario,
                "asunto": asunto,
                "mensaje": mensaje,
                "radicado": radicado,
                "dias_restantes": dias_restantes,
                "etapa": etapa,
                "enviado": enviado,
                "estado": estado
            }
        )


def obtener_historial():

    sql = text(
        """
        SELECT
            id,
            fecha_envio,
            tipo_alerta,
            radicado,
            etapa,
            dias_restantes,
            destinatario,
            asunto,
            estado,
            enviado
        FROM historial_alertas
        ORDER BY fecha_envio DESC
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()

def alerta_existe(
    tipo_alerta,
    asunto
):

    sql = text(
        """
        SELECT COUNT(*)
        FROM historial_alertas
        WHERE tipo_alerta = :tipo_alerta
        AND asunto = :asunto
        """
    )

    with engine.connect() as conn:

        cantidad = conn.execute(
            sql,
            {
                "tipo_alerta": tipo_alerta,
                "asunto": asunto
            }
        ).scalar()

        return cantidad > 0        

def contar_alertas_pendientes():

    sql = text(
        """
        SELECT COUNT(*)
        FROM historial_alertas
        WHERE estado = 'PENDIENTE'
        """
    )

    with engine.connect() as conn:

        return conn.execute(
            sql
        ).scalar()

def contar_alertas_criticas():

    sql = text(
        """
        SELECT COUNT(*)
        FROM historial_alertas
        WHERE dias_restantes  = 30
        """
    )

    with engine.connect() as conn:

        return conn.execute(
            sql         ).scalar()

def obtener_alertas_pendientes():

    sql = text(
        """
        SELECT
            id,
            tipo_alerta,
            destinatario,
            asunto,
            mensaje
        FROM historial_alertas
        WHERE estado = 'PENDIENTE'
        ORDER BY id
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()    

def actualizar_estado_alerta(
    id_alerta,
    estado
):

    sql = text(
        """
        UPDATE historial_alertas
        SET estado = :estado
        WHERE id = :id_alerta
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "id_alerta": id_alerta,
                "estado": estado
            }
        )

def contar_alertas_enviadas():

    sql = text(
        """
        SELECT COUNT(*)
        FROM historial_alertas
        WHERE estado = 'ENVIADA'
        """
    )

    with engine.connect() as conn:

        return conn.execute(
            sql
        ).scalar()

def contar_alertas_error():

    sql = text(
        """
        SELECT COUNT(*)
        FROM historial_alertas
        WHERE estado = 'ERROR'
        """
    )

    with engine.connect() as conn:

        return conn.execute(
            sql
        ).scalar()                