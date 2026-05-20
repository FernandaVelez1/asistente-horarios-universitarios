/* ============================================================
   MAIN.JS — Asistente de Horarios Universitarios
   Interacciones del formulario y mejoras de experiencia
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ----------------------------------------------------------
     1. EFECTO DE CARGA EN EL BOTON AL ENVIAR EL FORMULARIO
     ---------------------------------------------------------- */
  const form = document.getElementById('main-form');
  const submitBtn = document.getElementById('submit-btn');

  if (form && submitBtn) {
    form.addEventListener('submit', function (e) {
      // Validar que todos los campos requeridos esten llenos
      const camposRequeridos = form.querySelectorAll('[required]');
      let todoCompleto = true;

      camposRequeridos.forEach(function (campo) {
        if (!campo.value.trim()) {
          todoCompleto = false;
          campo.style.borderColor = '#c0392b';
          campo.style.boxShadow = '0 0 0 3px rgba(192, 57, 43, 0.12)';
        } else {
          campo.style.borderColor = '';
          campo.style.boxShadow = '';
        }
      });

      if (!todoCompleto) {
        e.preventDefault();
        mostrarMensaje('Por favor completa todos los campos antes de continuar.', 'error');
        return;
      }

      // Mostrar estado de carga
      submitBtn.classList.add('loading');
      submitBtn.textContent = 'Analizando datos';
    });
  }

  /* ----------------------------------------------------------
     2. LIMPIAR ESTILOS DE ERROR CUANDO EL USUARIO ESCRIBE
     ---------------------------------------------------------- */
  const camposTodos = document.querySelectorAll('input, select');
  camposTodos.forEach(function (campo) {
    campo.addEventListener('input', function () {
      this.style.borderColor = '';
      this.style.boxShadow = '';
    });
    campo.addEventListener('change', function () {
      this.style.borderColor = '';
      this.style.boxShadow = '';
    });
  });

  /* ----------------------------------------------------------
     3. SCROLL SUAVE HACIA RESULTADOS (si existen)
     ---------------------------------------------------------- */
  const seccionResultados = document.getElementById('resultados');
  if (seccionResultados) {
    setTimeout(function () {
      seccionResultados.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
  }

  /* ----------------------------------------------------------
     4. ANIMACION DE LAS BARRAS DEL HERO
     ---------------------------------------------------------- */
  const barras = document.querySelectorAll('.vc-bar');
  if (barras.length > 0) {
    function animarBarras() {
      const alturas = [
        ['55%', '85%', '40%', '95%', '60%'],
        ['70%', '50%', '80%', '45%', '90%'],
        ['60%', '80%', '45%', '90%', '65%'],
      ];
      let indice = 0;

      setInterval(function () {
        indice = (indice + 1) % alturas.length;
        barras.forEach(function (barra, i) {
          barra.style.height = alturas[indice][i];
        });
      }, 2500);
    }
    animarBarras();
  }

  /* ----------------------------------------------------------
     5. CONTADOR DE CARACTERES EN EL CAMPO DE MATERIAS
     ---------------------------------------------------------- */
  const campoMaterias = document.getElementById('materias_nombres');
  if (campoMaterias) {
    campoMaterias.addEventListener('input', function () {
      const partes = this.value.split(',').map(function (m) { return m.trim(); }).filter(Boolean);
      const hint = this.parentElement.querySelector('.field-hint');
      if (hint) {
        const cantidad = partes.length;
        if (cantidad > 0) {
          hint.textContent = cantidad + ' materia' + (cantidad !== 1 ? 's' : '') + ' detectada' + (cantidad !== 1 ? 's' : '');
          hint.style.color = '#2060a8';
        } else {
          hint.textContent = 'Separadas por comas';
          hint.style.color = '';
        }
      }
    });
  }

  /* ----------------------------------------------------------
     6. VALIDACION CRUZADA: HORAS DE SUENO
     ---------------------------------------------------------- */
  const campoSueno = document.getElementById('horas_sueno');
  if (campoSueno) {
    campoSueno.addEventListener('change', function () {
      const horas = parseFloat(this.value);
      const hint = this.parentElement.querySelector('.field-hint') ||
                   crearHint(this.parentElement);

      if (horas < 5) {
        hint.textContent = 'Atencion: menos de 5 horas puede afectar tu rendimiento';
        hint.style.color = '#c97a00';
      } else if (horas >= 7 && horas <= 9) {
        hint.textContent = 'Rango optimo para estudiantes';
        hint.style.color = '#1a7a4a';
      } else if (horas > 10) {
        hint.textContent = 'Dormir demasiado tambien puede reducir la productividad';
        hint.style.color = '#c97a00';
      } else {
        hint.textContent = '';
      }
    });
  }

  /* ----------------------------------------------------------
     7. FUNCION AUXILIAR: CREAR HINT DEBAJO DE UN INPUT
     ---------------------------------------------------------- */
  function crearHint(padre) {
    const span = document.createElement('span');
    span.classList.add('field-hint');
    padre.appendChild(span);
    return span;
  }

  /* ----------------------------------------------------------
     8. FUNCION AUXILIAR: MOSTRAR MENSAJE FLOTANTE
     ---------------------------------------------------------- */
  function mostrarMensaje(texto, tipo) {
    const existente = document.getElementById('mensaje-flotante');
    if (existente) existente.remove();

    const msg = document.createElement('div');
    msg.id = 'mensaje-flotante';
    msg.textContent = texto;
    msg.style.cssText = [
      'position: fixed',
      'bottom: 2rem',
      'left: 50%',
      'transform: translateX(-50%)',
      'background: ' + (tipo === 'error' ? '#c0392b' : '#163863'),
      'color: #fff',
      'padding: 12px 24px',
      'border-radius: 8px',
      'font-size: 0.875rem',
      'font-family: "DM Sans", sans-serif',
      'font-weight: 500',
      'box-shadow: 0 4px 20px rgba(0,0,0,0.2)',
      'z-index: 9999',
      'transition: opacity 0.3s ease',
    ].join(';');

    document.body.appendChild(msg);

    setTimeout(function () {
      msg.style.opacity = '0';
      setTimeout(function () { msg.remove(); }, 300);
    }, 3500);
  }

  /* ----------------------------------------------------------
     9. RESALTAR EL CAMPO DE MATERIA MAS DIFICIL SEGUN LA LISTA
     ---------------------------------------------------------- */
  const campoMateriaDificil = document.getElementById('materia_dificil');
  const campoNombres = document.getElementById('materias_nombres');

  if (campoMateriaDificil && campoNombres) {
    campoNombres.addEventListener('input', function () {
      const lista = this.value.split(',').map(function (m) { return m.trim(); }).filter(Boolean);
      if (lista.length > 0) {
        campoMateriaDificil.placeholder = 'Ej. ' + lista[0];
      }
    });
  }

});