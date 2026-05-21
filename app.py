# ============================================================
# APP.PY — Servidor principal Flask
# Asistente Inteligente de Horarios Universitarios
#
# Este archivo:
#   1. Recibe los datos del formulario HTML
#   2. Llama a logica.py (paradigma logico / Prolog)
#   3. Llama a funcional.py (paradigma funcional / Lisp)
#   4. Combina los resultados
#   5. Los manda de regreso al HTML para mostrarlos
# ============================================================

from flask import Flask, render_template, request
from logica import (
    evaluar_sobrecarga,
    horas_estudio_recomendadas,
    calidad_sueno,
    mejor_horario_estudio,
    prioridad_descanso,
    evaluar_carga_general,
)
from funcional import (
    calcular_horas_estudio,
    evaluar_riesgo,
    generar_recomendaciones,
    calcular_puntaje_bienestar,
    generar_horario_dia,
    detectar_condiciones,
    DIFICULTAD_A_NUM,
    ESTRES_A_NUM,
    ACTIVIDAD_A_NUM,
)

app = Flask(__name__)


# ------------------------------------------------------------
# RUTA PRINCIPAL: muestra el formulario
# ------------------------------------------------------------


@app.route("/")
def index():
    return render_template("index.html", resultado=None)


# ------------------------------------------------------------
# RUTA DE RESULTADO: procesa el formulario y genera respuesta
# ------------------------------------------------------------


@app.route("/resultado", methods=["POST"])
def resultado():
    # --------------------------------------------------------
    # PASO 1: Leer todos los datos que mando el formulario
    # --------------------------------------------------------
    try:
        num_materias = int(request.form.get("num_materias", 0))
        dificultad = request.form.get("dificultad", "media")
        materias_nombres = request.form.get("materias_nombres", "")
        horas_sueno = float(request.form.get("horas_sueno", 7))
        horas_libres = float(request.form.get("horas_libres", 4))
        horas_clases = float(request.form.get("horas_clases", 5))
        actividad_fisica = request.form.get("actividad_fisica", "poca")
        nivel_estres = request.form.get("nivel_estres", "moderado")
        semanas_examen = int(request.form.get("semanas_examen", 4))
        materia_dificil = request.form.get("materia_dificil", "")
        horario_preferido = request.form.get("horario_preferido", "tarde")
        metodo_estudio = request.form.get("metodo_estudio", "solo")
    except (ValueError, TypeError):
        # Si algo falla al leer los datos, mostrar pagina limpia
        return render_template(
            "index.html",
            resultado=None,
            error="Hubo un error al leer los datos. Intenta de nuevo.",
        )

    # --------------------------------------------------------
    # PASO 2: Convertir texto a numero para las funciones
    # --------------------------------------------------------
    dificultad_num = DIFICULTAD_A_NUM.get(dificultad, 2)
    estres_num = ESTRES_A_NUM.get(nivel_estres, 2)
    actividad_num = ACTIVIDAD_A_NUM.get(actividad_fisica, 1)
    tiene_actividad = actividad_num >= 2

    # --------------------------------------------------------
    # PASO 3: Llamar a las funciones de LOGICA (Prolog/Python)
    # --------------------------------------------------------

    # 3a. Detectar si hay sobrecarga
    hay_sobrecarga, msg_sobrecarga = evaluar_sobrecarga(
        num_materias, dificultad, horas_sueno, nivel_estres
    )

    # 3b. Horas de estudio (version logica)
    horas_logica = horas_estudio_recomendadas(dificultad, horas_libres)

    # 3c. Calidad del sueño
    calidad = calidad_sueno(horas_sueno)

    # 3d. Recomendacion de horario
    rec_horario = mejor_horario_estudio(horario_preferido)

    # 3e. Prioridad de descanso
    prioridad = prioridad_descanso(nivel_estres, horas_sueno)

    # 3f. Evaluacion de carga general
    carga_general = evaluar_carga_general(
        num_materias, dificultad, horas_sueno, nivel_estres, semanas_examen
    )

    # --------------------------------------------------------
    # PASO 4: Llamar a las funciones FUNCIONALES (Lisp/Python)
    # --------------------------------------------------------

    # 4a. Horas de estudio (version funcional — promedio con la logica)
    horas_funcional = calcular_horas_estudio(dificultad_num, horas_libres)
    horas_finales = round((horas_logica + horas_funcional) / 2, 1)

    # 4b. Nivel de riesgo funcional
    nivel_riesgo = evaluar_riesgo(estres_num, horas_sueno, num_materias)

    # 4c. Puntaje de bienestar
    puntaje_bienestar = calcular_puntaje_bienestar(
        horas_sueno, horas_libres, actividad_num
    )

    # 4d. Horario sugerido del dia
    horario_dia = generar_horario_dia(horario_preferido, horas_finales, tiene_actividad)

    # 4e. Detectar condiciones y generar recomendaciones con map()
    datos_para_condiciones = {
        "horas_sueno": horas_sueno,
        "estres_num": estres_num,
        "num_materias": num_materias,
        "dificultad_num": dificultad_num,
        "actividad_num": actividad_num,
        "semanas_examen": semanas_examen,
        "carga": carga_general,
    }
    condiciones_detectadas = detectar_condiciones(datos_para_condiciones)
    recomendaciones = generar_recomendaciones(condiciones_detectadas)

    # Agregar la recomendacion de horario al inicio de la lista
    recomendaciones.insert(0, rec_horario)

    # Agregar recomendacion sobre meteria mas dificil si aplica
    if materia_dificil and dificultad_num >= 3:
        recomendaciones.append(
            "Dedica sesiones específicas a {}: divide el tema en partes pequeñas.".format(
                materia_dificil
            )
        )

    # --------------------------------------------------------
    # PASO 5: Determinar si hay alerta y de que tipo
    # --------------------------------------------------------

    alerta = (
        hay_sobrecarga or nivel_riesgo in ("CRITICO", "ALTO") or puntaje_bienestar < 30
    )

    if nivel_riesgo == "CRITICO" or carga_general == "Critica":
        alerta_tipo = "critico"
        alerta_titulo = "Situacion de riesgo detectada"
        alerta_mensaje = (
            msg_sobrecarga
            if msg_sobrecarga
            else "Tu combinación actual de carga, sueño y estrés es peligrosa. Considera reducir actividades."
        )
    elif nivel_riesgo == "ALTO" or carga_general == "Alta":
        alerta_tipo = "advertencia"
        alerta_titulo = "Carga academica elevada"
        alerta_mensaje = "Tu situación actual requiere atención. Sigue las recomendaciones al pie de la letra."
    else:
        alerta_tipo = "positivo"
        alerta_titulo = "Situacion bajo control"
        alerta_mensaje = "Tu carga es manejable. Mantén tus hábitos y adelántate en las materias difíciles."

    # --------------------------------------------------------
    # PASO 6: Empaquetar todo en un diccionario y mandarlo al HTML
    # --------------------------------------------------------

    resultado = {
        # Numeros principales
        "horas_estudio": horas_finales,
        "prioridad_descanso": prioridad,
        "carga": carga_general,
        "puntaje_bienestar": puntaje_bienestar,
        "calidad_sueno": calidad,
        "nivel_riesgo": nivel_riesgo,
        # Alerta
        "alerta": alerta,
        "alerta_tipo": alerta_tipo,
        "alerta_titulo": alerta_titulo,
        "alerta_mensaje": alerta_mensaje,
        # Listas
        "recomendaciones": recomendaciones,
        "horario": horario_dia,
        # Datos originales (para mostrar en la pagina si se desea)
        "materias_nombres": materias_nombres,
        "materia_dificil": materia_dificil,
    }

    return render_template("index.html", resultado=resultado)


# ------------------------------------------------------------
# PUNTO DE ENTRADA — ejecutar el servidor
# ------------------------------------------------------------

if __name__ == "__main__":
    # debug=True muestra errores detallados en el navegador
    # Quitar debug=True cuando se suba a produccion
    app.run(debug=True, host="0.0.0.0", port=5000)
