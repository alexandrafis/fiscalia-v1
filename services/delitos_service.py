from sqlalchemy import text

from database.connection import engine


def guardar_delito(
    codigo,
    nombre,
    pena_maxima
):

    sql = text(
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
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "codigo": codigo,
                "nombre": nombre,
                "pena": pena_maxima
            }
        )


def obtener_delitos():

    sql = text(
        """
        SELECT
            id,
            codigo,
            nombre,
            pena_maxima_meses
        FROM delitos
        ORDER BY nombre
        """
    )

    with engine.begin() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()

def buscar_delito_por_codigo(
    codigo
):

    sql = text(
        """
        SELECT
            id,
            codigo,
            nombre,
            pena_maxima_meses
        FROM delitos
        WHERE UPPER(codigo) = UPPER(:codigo)
        """
    )

    with engine.begin() as conn:

        print("ENTRO A BUSCAR CODIGO")
        
        resultado = conn.execute(
            sql,
            {
                "codigo": codigo
            }
        )

        return resultado.fetchone()

def buscar_delito_por_nombre(
    nombre
):

    sql = text(
        """
        SELECT
            id,
            codigo,
            nombre,
            pena_maxima_meses
        FROM delitos
        WHERE TRIM(UPPER(nombre))
              =
              TRIM(UPPER(:nombre))
        """
    )

    with engine.begin() as conn:

        print("ENTRO A BUSCAR NOMBRE")

        resultado = conn.execute(
            sql,
            {
                "nombre": nombre
            }
        )

        return resultado.fetchone()