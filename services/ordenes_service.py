from sqlalchemy import text

from database.connection import engine


def guardar_orden(
    caso_id,
    numero_orden,
    tipo_orden,
    fecha_inicio,
    termino_dias,
    fecha_vencimiento,
    estado,
    semaforo
):

    sql = text(
        """
        INSERT INTO ordenes_pj
        (
            caso_id,
            numero_orden,
            tipo_orden,
            fecha_inicio,
            termino_dias,
            fecha_vencimiento,
            estado,
            semaforo
        )
        VALUES
        (
            :caso_id,
            :numero_orden,
            :tipo_orden,
            :fecha_inicio,
            :termino_dias,
            :fecha_vencimiento,
            :estado,
            :semaforo
        )
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "caso_id": caso_id,
                "numero_orden": numero_orden,
                "tipo_orden": tipo_orden,
                "fecha_inicio": fecha_inicio,
                "termino_dias": termino_dias,
                "fecha_vencimiento": fecha_vencimiento,
                "estado": estado,
                "semaforo": semaforo
            }
        )

def obtener_ordenes():

    sql = text(
        """
        SELECT
            numero_orden,
            caso_id,
            tipo_orden,
            fecha_vencimiento,
            estado,
            semaforo
        FROM ordenes_pj
        ORDER BY fecha_vencimiento
        """
    )

    with engine.connect() as conn:

        resultado = conn.execute(sql)

        return resultado.fetchall()

def eliminar_orden(
    numero_orden
):

    sql = text(
        """
        DELETE FROM ordenes_pj
        WHERE numero_orden = :numero_orden
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "numero_orden": numero_orden
            }
        )


def actualizar_estado_orden(
    numero_orden,
    estado
):

    sql = text(
        """
        UPDATE ordenes_pj
        SET estado = :estado
        WHERE numero_orden = :numero_orden
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "numero_orden": numero_orden,
                "estado": estado
            }
        )

def actualizar_orden(
    numero_orden,
    tipo_orden,
    fecha_inicio,
    termino_dias,
    fecha_vencimiento,
    estado,
    semaforo
):

    sql = text(
        """
        UPDATE ordenes_pj
        SET
            tipo_orden = :tipo_orden,
            fecha_inicio = :fecha_inicio,
            termino_dias = :termino_dias,
            fecha_vencimiento = :fecha_vencimiento,
            estado = :estado,
            semaforo = :semaforo
        WHERE numero_orden = :numero_orden
        """
    )

    with engine.begin() as conn:

        conn.execute(
            sql,
            {
                "numero_orden": numero_orden,
                "tipo_orden": tipo_orden,
                "fecha_inicio": fecha_inicio,
                "termino_dias": termino_dias,
                "fecha_vencimiento": fecha_vencimiento,
                "estado": estado,
                "semaforo": semaforo
            }
        )