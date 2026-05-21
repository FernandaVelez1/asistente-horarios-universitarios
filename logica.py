# ============================================================
# LOGICA.PY — Reglas logicas traducidas de Prolog a Python
#
# Este archivo representa el PARADIGMA LOGICO del proyecto.
# Las funciones aqui son equivalentes directas a las reglas
# definidas en prolog/reglas.pl
#
# En el proyecto academico, las reglas se DISEÑARON en Prolog
# y luego se tradujeron aqui para integrarse con Flask.
# ============================================================


def evaluar_sobrecarga(num_materias, dificultad, horas_sueno, nivel_estres):
    """
    Equivalente a la regla sobrecarga/4 de Prolog.
    Detecta si el estudiante tiene una carga insostenible.

    Retorna: (bool, str) -> (hay_sobrecarga, mensaje)
    """
    # Regla 1: muchas materias de alta dificultad
    if num_materias >= 6 and dificultad in ("alta", "muy_alta"):
        return (
            True,
            "La combinación de {} materias con dificultad {} representa una carga muy elevada.".format(
                num_materias, dificultad
            ),
        )

    # Regla 2: poco sueño + estrés alto
    if horas_sueno < 5 and nivel_estres in ("alto", "critico"):
        return (
            True,
            "Dormir {} horas con nivel de estrés {} es una combinación de riesgo para tu salud.".format(
                horas_sueno, nivel_estres
            ),
        )

    # Regla 3: situación crítica combinada
    if num_materias >= 7 and dificultad == "muy_alta" and horas_sueno < 6:
        return (
            True,
            "Situación crítica: {} materias muy difíciles con solo {} horas de sueño.".format(
                num_materias, horas_sueno
            ),
        )

    return False, ""


def horas_estudio_recomendadas(dificultad, horas_libres):
    """
    Equivalente a horas_estudio_recomendadas/3 de Prolog.
    Calcula cuantas horas estudiar segun la dificultad disponible.
    """
    factores = {
        "baja": (0.30, 2),
        "media": (0.45, 3),
        "alta": (0.60, 5),
        "muy_alta": (0.75, 6),
    }
    factor, maximo = factores.get(dificultad, (0.40, 3))
    horas = min(maximo, horas_libres * factor)
    return round(horas, 1)


def calidad_sueno(horas_sueno):
    """
    Equivalente a calidad_sueno/2 de Prolog.
    """
    if 7 <= horas_sueno <= 9:
        return "optimo"
    elif 6 <= horas_sueno < 7:
        return "aceptable"
    elif horas_sueno > 9:
        return "aceptable"
    elif 5 <= horas_sueno < 6:
        return "deficiente"
    else:
        return "critico"


def mejor_horario_estudio(horario_preferido):
    """
    Equivalente a mejor_horario_estudio/2 de Prolog.
    """
    recomendaciones = {
        "manana": "Estudia de 7am a 10am antes de clases, tu memoria está más fresca.",
        "tarde": "Estudia de 2pm a 5pm al terminar clases, mientras el material está fresco.",
        "noche": "Estudia de 8pm a 11pm, no pases de medianoche para proteger tu sueño.",
        "madrugada": "Advertencia: la madrugada daña la consolidación de memoria a largo plazo.",
    }
    return recomendaciones.get(
        horario_preferido, "Elige un horario fijo y mantenlo cada día."
    )


def prioridad_descanso(nivel_estres, horas_sueno):
    """
    Equivalente a prioridad_descanso/3 de Prolog.
    """
    if nivel_estres == "critico":
        return "Alta"
    if nivel_estres == "alto" and horas_sueno < 6:
        return "Alta"
    if nivel_estres == "alto" and horas_sueno >= 6:
        return "Media"
    return "Baja"


def evaluar_carga_general(
    num_materias, dificultad, horas_sueno, nivel_estres, semanas_examen
):
    """
    Regla compuesta: combina varias reglas logicas para dar
    una evaluacion general de la situacion del estudiante.

    Retorna: str ('Critica', 'Alta', 'Moderada', 'Manejable')
    """
    puntos = 0

    # Factores de riesgo (suman puntos negativos)
    if dificultad == "muy_alta":
        puntos += 3
    elif dificultad == "alta":
        puntos += 2
    elif dificultad == "media":
        puntos += 1

    if nivel_estres == "critico":
        puntos += 3
    elif nivel_estres == "alto":
        puntos += 2
    elif nivel_estres == "moderado":
        puntos += 1

    if horas_sueno < 5:
        puntos += 3
    elif horas_sueno < 6:
        puntos += 2
    elif horas_sueno < 7:
        puntos += 1

    if num_materias >= 7:
        puntos += 2
    elif num_materias >= 5:
        puntos += 1

    if semanas_examen <= 1:
        puntos += 2
    elif semanas_examen <= 2:
        puntos += 1

    # Clasificacion segun puntos acumulados
    if puntos >= 9:
        return "Critica"
    elif puntos >= 6:
        return "Alta"
    elif puntos >= 3:
        return "Moderada"
    else:
        return "Manejable"
