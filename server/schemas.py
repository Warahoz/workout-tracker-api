from marshmallow import Schema, fields, validate, validates, ValidationError
from models import Exercise, Workout, WorkoutExercise

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(
        required=True, 
        validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'Balance'])
    )
    equipment_needed = fields.Bool(load_default=False)

    # Nested workouts for single exercise GET /exercises/<id>
    workouts = fields.Nested('WorkoutSchema', many=True, only=('id', 'date', 'duration_minutes'), dump_only=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    # Single exercise data attached to a workout detail view
    exercise = fields.Nested('ExerciseSchema', only=('id', 'name', 'category', 'equipment_needed'), dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(allow_none=True)

    # Stretch goal: Include reps/sets/duration data from WorkoutExercises
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, dump_only=True)


# Instantiate Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=('workouts',))

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))

workout_exercise_schema = WorkoutExerciseSchema()