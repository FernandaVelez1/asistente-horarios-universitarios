const API = '';

let courses = [];
let schedules = [];

async function fetchCourses() {
    const res = await fetch(`${API}/api/courses`);
    courses = await res.json();
    renderCourses();
    renderRecommendCourses();
    renderScheduleCoursePickers();
}

async function fetchSchedules() {
    const res = await fetch(`${API}/api/schedules`);
    schedules = await res.json();
    renderSchedules();
}

function renderCourses() {
    const list = document.getElementById('courses-list');
    if (courses.length === 0) {
        list.innerHTML = '<p class="empty-msg">No hay materias registradas aún.</p>';
        return;
    }
    list.innerHTML = courses.map(c => `
        <div class="course-item">
            <div class="course-item-info">
                <h4>${c.name} <span class="badge">${c.code || 'Sin código'}</span></h4>
                <p>${c.professor ? 'Prof: ' + c.professor + ' · ' : ''}${c.credits} crédito(s)</p>
            </div>
            <button class="btn btn-danger" onclick="deleteCourse(${c.id})">Eliminar</button>
        </div>
    `).join('');
}

function renderRecommendCourses() {
    const list = document.getElementById('recommend-courses');
    if (courses.length === 0) {
        list.innerHTML = '<p class="empty-msg">Primero agrega materias en la pestaña "Materias".</p>';
        return;
    }
    list.innerHTML = courses.map(c => `
        <label class="checkbox-item">
            <input type="checkbox" value="${c.id}" name="rec-course">
            <span>${c.name}${c.code ? ' (' + c.code + ')' : ''} · ${c.credits} créditos</span>
        </label>
    `).join('');
}

function renderScheduleCoursePickers() {
    document.querySelectorAll('.item-course').forEach(select => {
        const current = select.value;
        select.innerHTML = courses.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
        if (current) select.value = current;
    });
}

function renderSchedules() {
    const list = document.getElementById('schedules-list');
    if (schedules.length === 0) {
        list.innerHTML = '<p class="empty-msg">No hay horarios guardados aún.</p>';
        return;
    }
    list.innerHTML = schedules.map(s => `
        <div class="schedule-item" style="flex-direction:column; align-items:flex-start;">
            <div style="display:flex; justify-content:space-between; width:100%; margin-bottom:8px;">
                <strong>${s.name}</strong>
                <button class="btn btn-danger" onclick="deleteSchedule(${s.id})">Eliminar</button>
            </div>
            ${s.items.length === 0 ? '<p style="font-size:0.85rem;color:#a0aec0;">Sin bloques de clase</p>' :
              s.items.map(item => `
                <div class="schedule-block">
                    <span class="course-name">${item.course ? item.course.name : 'Materia'}</span>
                    <span>${item.day}</span>
                    <span class="time">${item.start_time} – ${item.end_time}</span>
                    ${item.location ? '<span>' + item.location + '</span>' : ''}
                </div>
              `).join('')
            }
        </div>
    `).join('');
}

async function deleteCourse(id) {
    await fetch(`${API}/api/courses/${id}`, { method: 'DELETE' });
    await fetchCourses();
}

async function deleteSchedule(id) {
    await fetch(`${API}/api/schedules/${id}`, { method: 'DELETE' });
    await fetchSchedules();
}

document.getElementById('course-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('course-name').value.trim();
    const code = document.getElementById('course-code').value.trim();
    const professor = document.getElementById('course-professor').value.trim();
    const credits = parseInt(document.getElementById('course-credits').value);

    if (!name) return;

    await fetch(`${API}/api/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, code, professor, credits })
    });

    e.target.reset();
    document.getElementById('course-credits').value = 3;
    await fetchCourses();
});

document.getElementById('btn-recommend').addEventListener('click', async () => {
    const checked = [...document.querySelectorAll('input[name="rec-course"]:checked')];
    const course_ids = checked.map(cb => parseInt(cb.value));

    if (course_ids.length === 0) {
        alert('Selecciona al menos una materia para generar recomendaciones.');
        return;
    }

    const preferred_days = [...document.querySelectorAll('.days-selector input:checked')].map(cb => cb.value);

    const preferences = {
        avoid_early: document.getElementById('pref-avoid-early').checked,
        avoid_late: document.getElementById('pref-avoid-late').checked,
        preferred_days
    };

    const res = await fetch(`${API}/api/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ course_ids, preferences })
    });
    const data = await res.json();

    const resultDiv = document.getElementById('recommendations-result');
    const contentDiv = document.getElementById('recommendations-content');
    resultDiv.classList.remove('hidden');

    contentDiv.innerHTML = `
        <div class="summary-box">
            <p>${data.message}</p>
            <p>Total de créditos seleccionados: <strong>${data.total_credits}</strong></p>
        </div>
        ${data.recommendations.map(r => `
            <div class="recommendation-card">
                <h4>${r.course.name}${r.course.code ? ' (' + r.course.code + ')' : ''}</h4>
                <p>${r.suggestion}</p>
            </div>
        `).join('')}
    `;
});

document.getElementById('btn-add-item').addEventListener('click', () => {
    const container = document.getElementById('schedule-items-container');
    const newItem = document.createElement('div');
    newItem.className = 'schedule-item-entry';
    newItem.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4>Bloque de clase</h4>
            <button type="button" class="btn btn-danger" onclick="this.closest('.schedule-item-entry').remove()">Quitar</button>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Materia</label>
                <select class="item-course">${courses.map(c => `<option value="${c.id}">${c.name}</option>`).join('')}</select>
            </div>
            <div class="form-group">
                <label>Día</label>
                <select class="item-day">
                    <option>Lunes</option><option>Martes</option><option>Miércoles</option>
                    <option>Jueves</option><option>Viernes</option><option>Sábado</option>
                </select>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Hora inicio</label>
                <input type="time" class="item-start" value="08:00">
            </div>
            <div class="form-group">
                <label>Hora fin</label>
                <input type="time" class="item-end" value="10:00">
            </div>
            <div class="form-group">
                <label>Salón</label>
                <input type="text" class="item-location" placeholder="Ej: Aula 301">
            </div>
        </div>
    `;
    container.appendChild(newItem);
});

document.getElementById('schedule-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('schedule-name').value.trim();
    if (!name) return;

    const itemEntries = document.querySelectorAll('.schedule-item-entry');
    const items = [...itemEntries].map(entry => ({
        course_id: parseInt(entry.querySelector('.item-course').value),
        day: entry.querySelector('.item-day').value,
        start_time: entry.querySelector('.item-start').value,
        end_time: entry.querySelector('.item-end').value,
        location: entry.querySelector('.item-location').value
    })).filter(item => item.course_id);

    await fetch(`${API}/api/schedules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, items })
    });

    e.target.reset();
    document.getElementById('course-credits').value = 3;
    await fetchSchedules();
});

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
});

fetchCourses();
fetchSchedules();
