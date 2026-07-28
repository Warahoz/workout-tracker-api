#!/usr/bin/env python3

from datetime import date
from app import app
from models import *

with app.app_context():

    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    push_up = Exercise(name="Push-up", category="Strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="Strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="Balance", equipment_needed=False)
    treadmill_run = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)

    db.session.add_all([push_up, squat, plank, treadmill_run])
    db.session.commit()

    print("Seeding workouts...")
    workout_1 = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Morning strength session")
    workout_2 = Workout(date=date(2026, 7, 22), duration_minutes=30, notes="Quick cardio + core")

    db.session.add_all([workout_1, workout_2])
    db.session.commit()

    print("Seeding workout_exercises...")
    we_1 = WorkoutExercise(workout_id=workout_1.id, exercise_id=push_up.id, reps=15, sets=3)
    we_2 = WorkoutExercise(workout_id=workout_1.id, exercise_id=squat.id, reps=12, sets=4)
    we_3 = WorkoutExercise(workout_id=workout_2.id, exercise_id=treadmill_run.id, duration_seconds=900)
    we_4 = WorkoutExercise(workout_id=workout_2.id, exercise_id=plank.id, duration_seconds=60, sets=3)

    db.session.add_all([we_1, we_2, we_3, we_4])
    db.session.commit()

    print("Seeding complete!")