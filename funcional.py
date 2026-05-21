# ============================================================
# FUNCIONAL.PY — Funciones traducidas de Lisp (CLISP) a Python
#
# Este archivo representa el PARADIGMA FUNCIONAL del proyecto.
# Las funciones son equivalentes directas a las definidas
# en lisp/funciones.lisp
#
# Caracteristicas funcionales que se mantienen:
#   - Funciones puras (no modifican estado externo)
#   - Uso de map() equivalente a mapcar de Lisp
#   - Funciones lambda
#   - Listas como estructura principal de datos
# ============================================================

from functools import reduce


# ------------------------------------------------------------
# FUNCION 1: calcular_horas_estudio
# Equivalente a calcular-horas-estudio en Lisp
# Funcion pura: mismo input siempre produce mismo output
# ------------------------------------------------------------


def calcular_horas_estudio(dificultad_num, horas_libres):
    """
    dificultad_num: 1=baja, 2=media, 3=alta, 4=muy_alta
    horas_libres: numero de horas libres al dia
    Retorna: float con horas de estudio recomendadas
    """
    # Tabla de factores (equivalente al cond de Lisp)
    tabla = {1: (0.30, 2), 2: (0.45, 3), 3: (0.60, 5), 4: (0.75, 6)}
    factor, maximo = tabla.get(dificultad_num, (0.40, 3))
    return round(min(maximo, horas_libres * factor), 1)


# Mapa de conversion de texto a numero (para conectar con el formulario)
DIFICULTAD_A_NUM = {"baja": 1, "media": 2, "alta": 3, "muy_alta": 4}

ESTRES_A_NUM = {"bajo": 1, "moderado": 2, "alto": 3, "critico": 4}

ACTIVIDAD_A_NUM = {"ninguna": 0, "poca": 1, "moderada": 2, "alta": 3}


# ------------------------------------------------------------
# FUNCION 2: evaluar_riesgo
# Equivalente a evaluar-nivel-estres en Lisp
# Funcion pura con condicionales anidados (como cond de Lisp)
# ------------------------------------------------------------


def evaluar_riesgo(estres_num, horas_sueno, num_materias):
    """
    Retorna: str con nivel de riesgo general del estudiante
    """
    # Equivalente directo al cond de Lisp
    if estres_num >= 3 and horas_sueno < 5:
        return "CRITICO"
    elif estres_num >= 3 and num_materias >= 6:
        return "ALTO"
    elif estres_num == 2 and horas_sueno < 6:
        return "MODERADO-RIESGO"
    elif estres_num == 4:
        return "CRITICO"
    elif estres_num == 3:
        return "ALTO"
    elif estres_num == 2:
        return "MODERADO"
    else:
        return "BAJO"


# ------------------------------------------------------------
# FUNCION 3: generar_recomendaciones
# Equivalente a generar-recomendaciones en Lisp
# Uso de map() — equivalente a mapcar de Lisp
# ------------------------------------------------------------

# Diccionario de recomendaciones (equivalente a los hechos del cond de Lisp)
BANCO_RECOMENDACIONES = {
    "poco_sueno": "Duerme al menos 7 horas. La memoria consolida información durante el sueño.",
    "estres_alto": "Toma descansos activos de 10 minutos cada hora de estudio.",
    "muchas_materias": "Divide el estudio por bloques: una materia diferente cada 90 minutos.",
    "dificultad_alta": "Prioriza la materia más difícil en tu horario de mayor concentración.",
    "sin_actividad": "Incluye 30 minutos de caminata. Mejora la concentración hasta un 20%.",
    "examen_proximo": "Con examen en menos de 2 semanas, enfoca el 70% del tiempo en esa materia.",
    "carga_critica": "Considera hablar con un asesor académico para reducir tu carga.",
    "horario_irregular": "Mantén un horario de estudio fijo. El cerebro aprende mejor con rutina.",
    "buena_condicion": "Vas bien. Sigue manteniendo tus hábitos y no bajes la guardia.",
}


def texto_recomendacion(condicion):
    """Equivalente a la funcion texto-recomendacion de Lisp"""
    return BANCO_RECOMENDACIONES.get(
        condicion, "Mantén un horario constante y descansa bien."
    )


def generar_recomendaciones(lista_condiciones):
    """
    Usa map() exactamente como mapcar en Lisp:
        (mapcar #'texto-recomendacion lista-condiciones)
    """
    return list(map(texto_recomendacion, lista_condiciones))


# ------------------------------------------------------------
# FUNCION 4: calcular_puntaje_bienestar
# Equivalente a calcular-puntaje-bienestar en Lisp
# Usa reduce() — equivalente a la recursion de sumar-lista en Lisp
# ------------------------------------------------------------


def calcular_puntaje_bienestar(horas_sueno, horas_libres, actividad_num):
    """
    Retorna: int entre 0 y 80 indicando bienestar general
    """
    factores = [
        30 if horas_sueno >= 7 else round(horas_sueno * 3),
        25 if horas_libres >= 3 else round(horas_libres * 6),
        {3: 25, 2: 15, 1: 8, 0: 0}.get(actividad_num, 0),
    ]
    # reduce() equivale a la recursion sumar-lista de Lisp
    return reduce(lambda acc, x: acc + x, factores, 0)


# ------------------------------------------------------------
# FUNCION 5: generar_horario_dia
# Equivalente a generar-horario-dia en Lisp
# Retorna lista de diccionarios (hora, actividad)
# ------------------------------------------------------------


def generar_horario_dia(horario_pref, horas_estudio, tiene_actividad):
    """
    Retorna: lista de dicts con 'hora' y 'actividad'
    """
    bloque_estudio_1 = "Estudio ({} h bloque 1)".format(min(2, horas_estudio))
    bloque_estudio_n = "Estudio ({} h)".format(horas_estudio)
    bloque_actividad = "Actividad física" if tiene_actividad else "Tiempo libre"

    horarios = {
        "manana": [
            {"hora": "6:00 - 7:00", "actividad": "Despertar y desayuno"},
            {"hora": "7:00 - 9:00", "actividad": bloque_estudio_1},
            {"hora": "9:00 - 13:00", "actividad": "Clases"},
            {"hora": "13:00 - 14:00", "actividad": "Comida y descanso"},
            {"hora": "14:00 - 16:00", "actividad": "Repaso y tareas"},
            {"hora": "16:00 - 17:00", "actividad": bloque_actividad},
            {"hora": "21:00 - 22:00", "actividad": "Lectura ligera"},
            {"hora": "22:00", "actividad": "Dormir"},
        ],
        "tarde": [
            {"hora": "7:30 - 8:00", "actividad": "Despertar y desayuno"},
            {"hora": "8:00 - 13:00", "actividad": "Clases"},
            {"hora": "13:00 - 14:30", "actividad": "Comida"},
            {"hora": "14:30 - 18:00", "actividad": bloque_estudio_n},
            {"hora": "18:00 - 19:00", "actividad": bloque_actividad},
            {"hora": "19:00 - 20:00", "actividad": "Cena"},
            {"hora": "20:00 - 21:00", "actividad": "Tiempo libre"},
            {"hora": "22:30", "actividad": "Dormir"},
        ],
        "noche": [
            {"hora": "7:00 - 8:00", "actividad": "Despertar y desayuno"},
            {"hora": "8:00 - 13:00", "actividad": "Clases"},
            {"hora": "13:00 - 15:00", "actividad": "Comida y descanso"},
            {"hora": "15:00 - 17:00", "actividad": "Tiempo libre"},
            {"hora": "17:00 - 18:00", "actividad": bloque_actividad},
            {"hora": "19:00 - 20:00", "actividad": "Cena"},
            {"hora": "20:00 - 23:00", "actividad": bloque_estudio_n},
            {"hora": "23:00", "actividad": "Dormir — no pases de esta hora"},
        ],
        "madrugada": [
            {"hora": "8:00 - 9:00", "actividad": "Despertar (tarde)"},
            {"hora": "9:00 - 13:00", "actividad": "Clases"},
            {"hora": "13:00 - 14:00", "actividad": "Comida"},
            {"hora": "14:00 - 17:00", "actividad": bloque_estudio_n},
            {"hora": "17:00 - 20:00", "actividad": "Tiempo libre"},
            {"hora": "20:00 - 21:00", "actividad": "Cena"},
            {"hora": "21:00 - 23:00", "actividad": "Actividad tranquila"},
            {
                "hora": "23:00",
                "actividad": "ADVERTENCIA: intenta dormir antes de la 1am",
            },
        ],
    }
    return horarios.get(horario_pref, horarios["tarde"])


# ------------------------------------------------------------
# FUNCION 6: detectar_condiciones
# Funcion auxiliar que determina que condiciones aplican
# para luego pasarlas a generar_recomendaciones()
# ------------------------------------------------------------


def detectar_condiciones(datos):
    """
    Recibe el diccionario de datos del formulario.
    Retorna: lista de claves de condiciones detectadas.
    """
    condiciones = []

    if datos["horas_sueno"] < 6:
        condiciones.append("poco_sueno")
    if datos["estres_num"] >= 3:
        condiciones.append("estres_alto")
    if datos["num_materias"] >= 6:
        condiciones.append("muchas_materias")
    if datos["dificultad_num"] >= 3:
        condiciones.append("dificultad_alta")
    if datos["actividad_num"] == 0:
        condiciones.append("sin_actividad")
    if datos["semanas_examen"] <= 2:
        condiciones.append("examen_proximo")
    if datos["carga"] in ("Critica", "Alta"):
        condiciones.append("carga_critica")
    if not condiciones:
        condiciones.append("buena_condicion")

    return condiciones
