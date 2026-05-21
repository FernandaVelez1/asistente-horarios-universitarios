; ============================================================
; FUNCIONES LISP — Asistente de Horarios Universitarios
; Este archivo se ejecuta en JDoodle CLISP online:
; https://www.jdoodle.com/execute-clisp-online
;
; COMO USARLO EN CLASE:
;   1. Ir a https://www.jdoodle.com/execute-clisp-online
;   2. Pegar este codigo completo
;   3. Hacer clic en Execute
;   4. Ver los resultados en la caja de salida
; ============================================================


; ------------------------------------------------------------
; FUNCION 1: calcular-horas-estudio
; Recibe: dificultad (1=baja, 2=media, 3=alta, 4=muy_alta)
;         horas-libres (numero)
; Devuelve: horas de estudio recomendadas
;
; Este es un ejemplo de programacion funcional pura:
; la funcion no modifica nada externo, solo calcula y retorna.
; ------------------------------------------------------------

(defun calcular-horas-estudio (dificultad horas-libres)
  (let ((factor (cond
                  ((= dificultad 1) 0.30)
                  ((= dificultad 2) 0.45)
                  ((= dificultad 3) 0.60)
                  ((= dificultad 4) 0.75)
                  (t 0.40))))
    (let ((maximo (cond
                    ((= dificultad 1) 2)
                    ((= dificultad 2) 3)
                    ((= dificultad 3) 5)
                    ((= dificultad 4) 6)
                    (t 3))))
      (min maximo (* horas-libres factor)))))


; ------------------------------------------------------------
; FUNCION 2: evaluar-nivel-estres
; Recibe: estres-num (1=bajo, 2=moderado, 3=alto, 4=critico)
;         horas-sueno (numero)
;         num-materias (entero)
; Devuelve: una cadena con el nivel de riesgo general
; ------------------------------------------------------------

(defun evaluar-nivel-estres (estres-num horas-sueno num-materias)
  (cond
    ((and (>= estres-num 3) (< horas-sueno 5)) "CRITICO")
    ((and (>= estres-num 3) (>= num-materias 6)) "ALTO")
    ((and (= estres-num 2) (< horas-sueno 6)) "MODERADO-RIESGO")
    ((= estres-num 4) "CRITICO")
    ((= estres-num 3) "ALTO")
    ((= estres-num 2) "MODERADO")
    (t "BAJO")))


; ------------------------------------------------------------
; FUNCION 3: generar-recomendaciones
; Uso de mapcar (funcion de orden superior de Lisp)
; Recibe: lista de condiciones como simbolos
; Devuelve: lista de textos de recomendacion
;
; mapcar aplica una funcion a cada elemento de una lista,
; esto es caracteristico de la programacion funcional.
; ------------------------------------------------------------

(defun texto-recomendacion (condicion)
  (cond
    ((eq condicion 'poco-sueno)
     "Duerme al menos 7 horas. La memoria consolida informacion durante el sueno.")
    ((eq condicion 'estres-alto)
     "Toma descansos activos de 10 minutos cada hora de estudio.")
    ((eq condicion 'muchas-materias)
     "Divide el estudio por bloques: una materia diferente cada 90 minutos.")
    ((eq condicion 'dificultad-alta)
     "Prioriza la materia mas dificil en tu horario de mayor concentracion.")
    ((eq condicion 'sin-actividad)
     "Incluye 30 minutos de caminata. Mejora la concentracion hasta un 20%.")
    ((eq condicion 'examen-proximo)
     "Con examen en menos de 2 semanas, enfoca el 70% del tiempo en esa materia.")
    (t "Mantén un horario constante, tu cerebro aprende mejor con rutina.")))

(defun generar-recomendaciones (lista-condiciones)
  (mapcar #'texto-recomendacion lista-condiciones))


; ------------------------------------------------------------
; FUNCION 4: calcular-puntaje-bienestar
; Funcion recursiva — otro pilar de la programacion funcional
; Suma una lista de factores de bienestar
; ------------------------------------------------------------

(defun sumar-lista (lista)
  (if (null lista)
      0
      (+ (car lista) (sumar-lista (cdr lista)))))

(defun calcular-puntaje-bienestar (horas-sueno horas-libres nivel-actividad)
  (let ((factores (list
                    (if (>= horas-sueno 7) 30 (* horas-sueno 3))
                    (if (>= horas-libres 3) 25 (* horas-libres 6))
                    (cond
                      ((= nivel-actividad 3) 25)
                      ((= nivel-actividad 2) 15)
                      ((= nivel-actividad 1) 8)
                      (t 0)))))
    (sumar-lista factores)))


; ------------------------------------------------------------
; FUNCION 5: generar-horario-dia
; Genera una lista de bloques de actividad para el dia
; Uso de funciones de lista propias de Lisp
; ------------------------------------------------------------

(defun generar-horario-dia (horario-pref horas-estudio tiene-actividad)
  (cond
    ((string= horario-pref "manana")
     (list
       '("6:00 - 7:00"  "Despertar y desayuno")
       (list "7:00 - 9:00"  (format nil "Estudio (~A horas bloque 1)" (min 2 horas-estudio)))
       '("9:00 - 10:00" "Clases")
       '("12:00 - 13:00" "Descanso y comida")
       '("13:00 - 15:00" "Repaso y tareas")
       (if tiene-actividad
           '("16:00 - 17:00" "Actividad fisica")
           '("16:00 - 17:00" "Tiempo libre"))
       '("21:00 - 22:00" "Lectura ligera antes de dormir")
       '("22:00"         "Dormir")))
    ((string= horario-pref "noche")
     (list
       '("7:00 - 8:00"   "Despertar y desayuno")
       '("8:00 - 13:00"  "Clases")
       '("13:00 - 14:00" "Comida y descanso")
       '("14:00 - 16:00" "Tiempo libre o siestas cortas")
       (if tiene-actividad
           '("17:00 - 18:00" "Actividad fisica")
           '("17:00 - 18:00" "Descanso activo"))
       '("19:00 - 20:00" "Cena")
       (list "20:00 - 23:00" (format nil "Estudio (~A horas)" horas-estudio))
       '("23:00"         "Dormir - no pases de esta hora")))
    (t
     (list
       '("7:00"          "Despertar")
       '("8:00 - 13:00"  "Clases")
       '("13:00 - 15:00" "Comida y descanso")
       (list "15:00 - 18:00" (format nil "Estudio (~A horas)" horas-estudio))
       '("18:00 - 21:00" "Tiempo libre")
       '("21:00 - 22:00" "Repaso rapido")
       '("22:30"         "Dormir")))))


; ============================================================
; SECCION DE PRUEBAS — Se ejecutan al correr el archivo
; ============================================================

(format t "~%=== PRUEBAS DE FUNCIONES LISP ===~%~%")

; Prueba 1
(format t "Horas de estudio (dificultad alta, 5h libres): ~A h~%"
        (calcular-horas-estudio 3 5))

; Prueba 2
(format t "Nivel de riesgo (estres=3, sueno=4.5h, 7 materias): ~A~%"
        (evaluar-nivel-estres 3 4.5 7))

; Prueba 3
(format t "~%Recomendaciones generadas:~%")
(let ((recs (generar-recomendaciones
              '(poco-sueno estres-alto muchas-materias examen-proximo))))
  (mapcar (lambda (r) (format t "  - ~A~%" r)) recs))

; Prueba 4
(format t "~%Puntaje de bienestar (7h sueno, 4h libres, actividad moderada): ~A / 80~%"
        (calcular-puntaje-bienestar 7 4 2))

; Prueba 5
(format t "~%Horario sugerido (preferencia: noche):~%")
(let ((horario (generar-horario-dia "noche" 4 t)))
  (mapcar (lambda (bloque)
            (format t "  ~A — ~A~%" (first bloque) (second bloque)))
          horario))

(format t "~%=== FIN DE PRUEBAS ===~%")