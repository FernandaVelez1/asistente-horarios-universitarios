% ============================================================
% REGLAS PROLOG — Asistente de Horarios Universitarios
% Este archivo se ejecuta en SWISH (swish.swi-prolog.org)
% para demostrar el paradigma de programacion logica.
%
% COMO USARLO EN CLASE:
%   1. Ir a https://swish.swi-prolog.org
%   2. Pegar este codigo en el editor
%   3. Hacer consultas en la caja de abajo
% ============================================================


% ------------------------------------------------------------
% HECHOS: niveles validos del sistema
% ------------------------------------------------------------

nivel_estres(bajo).
nivel_estres(moderado).
nivel_estres(alto).
nivel_estres(critico).

dificultad(baja).
dificultad(media).
dificultad(alta).
dificultad(muy_alta).

horario(manana).
horario(tarde).
horario(noche).
horario(madrugada).


% ------------------------------------------------------------
% REGLAS: detectar sobrecarga academica
%
% Un estudiante tiene sobrecarga si:
%   - Tiene muchas materias Y dificultad alta
%   - O duerme poco Y tiene estres alto
%   - O combina todo lo anterior
% ------------------------------------------------------------

sobrecarga(Materias, Dificultad, HorasSueno, Estres) :-
    Materias >= 6,
    (Dificultad = alta ; Dificultad = muy_alta),
    write('Alerta: carga academica elevada detectada'), nl.

sobrecarga(_, _, HorasSueno, Estres) :-
    HorasSueno < 5,
    (Estres = alto ; Estres = critico),
    write('Alerta: combinacion peligrosa de poco sueno y estres alto'), nl.

sobrecarga(Materias, Dificultad, HorasSueno, _) :-
    Materias >= 7,
    Dificultad = muy_alta,
    HorasSueno < 6,
    write('Alerta critica: riesgo de agotamiento severo'), nl.


% ------------------------------------------------------------
% REGLAS: recomendar horas de estudio por dia
%
% Logica: a mas dificultad y menos tiempo libre, mas horas
% ------------------------------------------------------------

horas_estudio_recomendadas(baja,   HorasLibres, Horas) :-
    Horas is min(2, HorasLibres * 0.3).

horas_estudio_recomendadas(media,  HorasLibres, Horas) :-
    Horas is min(3, HorasLibres * 0.45).

horas_estudio_recomendadas(alta,   HorasLibres, Horas) :-
    Horas is min(5, HorasLibres * 0.6).

horas_estudio_recomendadas(muy_alta, HorasLibres, Horas) :-
    Horas is min(6, HorasLibres * 0.75).


% ------------------------------------------------------------
% REGLAS: evaluar calidad del descanso
% ------------------------------------------------------------

calidad_sueno(HorasSueno, optimo) :-
    HorasSueno >= 7, HorasSueno =< 9.

calidad_sueno(HorasSueno, aceptable) :-
    HorasSueno >= 6, HorasSueno < 7.

calidad_sueno(HorasSueno, aceptable) :-
    HorasSueno > 9.

calidad_sueno(HorasSueno, deficiente) :-
    HorasSueno >= 5, HorasSueno < 6.

calidad_sueno(HorasSueno, critico) :-
    HorasSueno < 5.


% ------------------------------------------------------------
% REGLAS: recomendar momento de estudio
% ------------------------------------------------------------

mejor_horario_estudio(manana,    'Estudia de 7am a 10am antes de clases').
mejor_horario_estudio(tarde,     'Estudia de 2pm a 5pm al terminar clases').
mejor_horario_estudio(noche,     'Estudia de 8pm a 11pm, no pases de medianoche').
mejor_horario_estudio(madrugada, 'Advertencia: la madrugada daña la memoria a largo plazo').


% ------------------------------------------------------------
% REGLAS: nivel de prioridad de descanso
% ------------------------------------------------------------

prioridad_descanso(critico,  _, Alta)  :- Alta = alta.
prioridad_descanso(alto,     HorasSueno, Alta) :-
    HorasSueno < 6, Alta = alta.
prioridad_descanso(alto,     HorasSueno, Media) :-
    HorasSueno >= 6, Media = media.
prioridad_descanso(moderado, _, Baja)  :- Baja = baja.
prioridad_descanso(bajo,     _, Baja)  :- Baja = baja.


% ------------------------------------------------------------
% CONSULTAS DE EJEMPLO para usar en SWISH
%
% Copia estas lineas una por una en la caja de consultas:
%
% ?- horas_estudio_recomendadas(alta, 5, H).
% ?- calidad_sueno(6.5, Calidad).
% ?- sobrecarga(7, muy_alta, 4, critico).
% ?- mejor_horario_estudio(noche, Recomendacion).
% ?- prioridad_descanso(alto, 5, Nivel).
% ------------------------------------------------------------