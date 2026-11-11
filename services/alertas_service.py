from sqlalchemy import text

from database.connection import engine

from services.historial_alertas_service import (
    registrar_alerta,
    alerta_existe,
    obtener_alertas_pendientes,
    actualizar_estado_alerta
)

from services.destinatarios_alertas_service import (
    obtener_destinatarios_indagacion
)

from services.graph_email_service import (
    enviar_correo
)

from datetime import date

from services.configuracion_alertas_service import (
    obtener_configuracion
)

def generar_alertas_indagacion():

    sql = text(
        """
        SELECT
            radicado,
            fecha_prescripcion
        FROM casos
        WHERE etapa_actual = 'INDAGACION'
        """
    )

    with engine.connect() as conn:

        resultados = conn.execute(
            sql
        ).fetchall()

    config = obtener_configuracion()

    destinatarios = (
        obtener_destinatarios_indagacion()
    )

    dias_configurados = [
        config.indagacion_1,
        config.indagacion_2,
        config.indagacion_3,
        config.indagacion_4
    ]
    for caso in resultados:
        
        dias_restantes = (
            caso.fecha_prescripcion - date.today()
        ).days

        # if dias_restantes not in dias_configurados:
        #    continue

        for destinatario in destinatarios:
            
            registrar_alerta(
                tipo_alerta="INDAGACION",
                destinatario=destinatario.correo,
                asunto=f"Alerta de Prescripción {caso.radicado}",
                mensaje=(
                    f"El caso {caso.radicado} "
                    f"se encuentra a "
                    f"{dias_restantes} días "
                    f"de prescribir."
                ),
                radicado=caso.radicado,
                dias_restantes=dias_restantes,
                etapa="INDAGACION",
                enviado=False
            )

def generar_alertas_juicio():

    sql = text(
        """
        SELECT
            radicado,
            fecha_prescripcion
        FROM casos
        WHERE etapa_actual = 'JUICIO'
        """
    )

    with engine.connect() as conn:

        resultados = conn.execute(
            sql
        ).fetchall()

    config = obtener_configuracion()

    dias_configurados = [
        config.juicio_1,
        config.juicio_2,
        config.juicio_3,
        config.juicio_4
    ]

    for caso in resultados:

        dias_restantes = (
            caso.fecha_prescripcion - date.today()
        ).days

        if dias_restantes not in dias_configurados:
            continue

        asunto = (
            f"Alerta de Prescripción {caso.radicado}"
        )

        if not alerta_existe(
            "JUICIO",
            asunto
        ):

            registrar_alerta(
                tipo_alerta="JUICIO",
                destinatario="pendiente",
                asunto=asunto,
                mensaje=(
                    f"El caso {caso.radicado} "
                    f"se encuentra a "
                    f"{dias_restantes} días "
                    f"de prescribir."
                ),
                enviado=False
            )

def generar_alertas_ordenes_pj():

    sql = text(
        """
        SELECT
            numero_orden,
            fecha_vencimiento
        FROM ordenes_pj
        """
    )

    with engine.connect() as conn:

        resultados = conn.execute(
            sql
        ).fetchall()

    config = obtener_configuracion()

    dias_configurados = [
        config.alerta_orden_1,
        config.alerta_orden_2,
        config.alerta_orden_3,
        config.alerta_orden_4
    ]

    for orden in resultados:

        dias_restantes = (
            orden.fecha_vencimiento - date.today()
        ).days

        if dias_restantes not in dias_configurados:
            continue

        asunto = (
            f"Orden PJ próxima a vencer {orden.numero_orden}"
        )

        if not alerta_existe(
            "ORDEN_PJ",
            asunto
        ):

            registrar_alerta(
                tipo_alerta="ORDEN_PJ",
                destinatario="pendiente",
                asunto=asunto,
                mensaje=(
                    f"La orden PJ "
                    f"{orden.numero_orden} "
                    f"vence en "
                    f"{dias_restantes} días."
                ),
                enviado=False
            )

def procesar_alertas_pendientes():

    alertas = obtener_alertas_pendientes()

    for alerta in alertas:

        try:

            enviado = enviar_correo(
                alerta.destinatario,
                alerta.asunto,
                alerta.mensaje
            )

            if enviado:

                actualizar_estado_alerta(
                    alerta.id,
                    "ENVIADA"
                )

            else:

                actualizar_estado_alerta(
                    alerta.id,
                    "ERROR"
                )

        except Exception:

            actualizar_estado_alerta(
                alerta.id,
                "ERROR"
            )