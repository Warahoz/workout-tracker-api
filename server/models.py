from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'

    VALID_CATEGORIES = [ 'Cardio', 'Strength', 'Flexibility', 'Balance']

    @validates('category')
    def validate_category(self, key, value):
        if value not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of {self.VALID_CATEGORIES}")
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be blank")
        return value
    
class Workout(db.Model):
    __tablename__= 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    __table_args__= (
        db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
        db.CheckConstraint('duration_minutes <= 600', name='check_duration_max')
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be a positive integer")
        if value > 600:
            raise ValueError("Workout duration seem unrealistic (max 600 minutes)")
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'
