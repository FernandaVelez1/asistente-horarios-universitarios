from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), default='')
    professor = db.Column(db.String(200), default='')
    credits = db.Column(db.Integer, default=3)

    schedule_items = db.relationship('ScheduleItem', backref='course', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'professor': self.professor,
            'credits': self.credits
        }


class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    items = db.relationship('ScheduleItem', backref='schedule', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.to_dict() for item in self.items]
        }


class ScheduleItem(db.Model):
    __tablename__ = 'schedule_items'

    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), default='')

    def to_dict(self):
        return {
            'id': self.id,
            'schedule_id': self.schedule_id,
            'course_id': self.course_id,
            'course': self.course.to_dict() if self.course else None,
            'day': self.day,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location
        }
