from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    VALID_CATEGORIES = ['Cardio', 'Strength', 'Flexibility', 'Balance']

    # relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

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

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
        db.CheckConstraint('duration_minutes <= 600', name='check_duration_max')
    )

    # relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be a positive integer")
        if value > 600:
            raise ValueError("Workout duration seems unrealistic (max 600 minutes)")
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.CheckConstraint('reps IS NULL OR reps > 0', name='check_reps_positive'),
        db.CheckConstraint('sets IS NULL OR sets > 0', name='check_sets_positive'),
    )

    # relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be a positive number")
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}>'