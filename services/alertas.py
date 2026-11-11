from datetime import date


def calcular_dias_restantes(
    fecha_prescripcion
):

    hoy = date.today()

    return (
        fecha_prescripcion - hoy
    ).days


def calcular_semaforo(
    dias_restantes
):

    if dias_restantes <= 0:
        return "NEGRO"

    if dias_restantes <= 30:
        return "ROJO"

    if dias_restantes <= 180:
        return "NARANJA"

    if dias_restantes <= 365:
        return "AMARILLO"

    return "VERDE"