from dateutil.relativedelta import relativedelta


def calcular_prescripcion_indagacion(
    fecha_hechos,
    pena_maxima_meses
):
    return (
        fecha_hechos +
        relativedelta(
            months=pena_maxima_meses
        )
    )


def calcular_prescripcion_juicio(
    fecha_acusacion,
    pena_maxima_meses
):
    return (
        fecha_acusacion +
        relativedelta(
            months=(pena_maxima_meses // 2)
        )
    )