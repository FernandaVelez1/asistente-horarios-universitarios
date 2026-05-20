from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, Course, Schedule, ScheduleItem
import os

app = Flask(__name__)
CORS(app)

database_url = os.environ.get('DATABASE_URL', 'sqlite:///schedules.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])

@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    course = Course(
        name=data['name'],
        code=data.get('code', ''),
        professor=data.get('professor', ''),
        credits=data.get('credits', 3)
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted'})

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.all()
    return jsonify([s.to_dict() for s in schedules])

@app.route('/api/schedules', methods=['POST'])
def create_schedule():
    data = request.get_json()
    schedule = Schedule(name=data['name'])
    db.session.add(schedule)
    db.session.flush()

    for item_data in data.get('items', []):
        item = ScheduleItem(
            schedule_id=schedule.id,
            course_id=item_data['course_id'],
            day=item_data['day'],
            start_time=item_data['start_time'],
            end_time=item_data['end_time'],
            location=item_data.get('location', '')
        )
        db.session.add(item)

    db.session.commit()
    return jsonify(schedule.to_dict()), 201

@app.route('/api/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule deleted'})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    selected_course_ids = data.get('course_ids', [])
    preferences = data.get('preferences', {})

    courses = Course.query.filter(Course.id.in_(selected_course_ids)).all()

    days_order = {'Lunes': 0, 'Martes': 1, 'Miércoles': 2, 'Jueves': 3, 'Viernes': 4}
    avoid_early = preferences.get('avoid_early', False)
    avoid_late = preferences.get('avoid_late', False)
    preferred_days = preferences.get('preferred_days', [])

    recommendations = []
    for course in courses:
        rec = {
            'course': course.to_dict(),
            'suggestion': f'Materia {course.name} ({course.credits} créditos) lista para asignar horario.'
        }
        recommendations.append(rec)

    return jsonify({
        'recommendations': recommendations,
        'total_credits': sum(c.credits for c in courses),
        'message': f'Se generaron recomendaciones para {len(courses)} materias.'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
