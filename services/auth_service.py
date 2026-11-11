from sqlalchemy import text

from database.connection import engine


def validar_usuario(
    usuario,
    clave
):

    sql = text(
        """
        SELECT
            id,
            usuario,
            rol
        FROM seguridad_usuarios
        WHERE usuario = :usuario
        AND clave = :clave
        AND habilitado = TRUE
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(
            sql,
            {
                "usuario": usuario,
                "clave": clave
            }
        )

        return resultado.fetchone()