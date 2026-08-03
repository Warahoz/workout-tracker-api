from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from datetime import datetime
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, 
    exercises_schema, 
    workout_schema, 
    workouts_schema, 
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# ------------------------------------------------------------------
# WORKOUT ENDPOINTS
# ------------------------------------------------------------------

@app.route('/workouts', methods=['GET', 'POST'])
def handle_workouts():
    if request.method == 'GET':
        workouts = Workout.query.all()
        return make_response(workouts_schema.dump(workouts), 200)

    elif request.method == 'POST':
        json_data = request.get_json() or {}
        
        # Parse date string if passed
        if 'date' in json_data and isinstance(json_data['date'], str):
            try:
                json_data['date'] = datetime.strptime(json_data['date'], '%Y-%m-%d').date()
            except ValueError:
                return make_response(jsonify({"errors": ["Date must be in YYYY-MM-DD format."]}), 400)
                
        try:
            validated_data = workout_schema.load(json_data)
            new_workout = Workout(**validated_data)
            db.session.add(new_workout)
            db.session.commit()
            return make_response(workout_schema.dump(new_workout), 201)
        except ValidationError as err:
            return make_response(jsonify({"errors": err.messages}), 422)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": [str(e)]}), 400)


@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def handle_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    if request.method == 'GET':
        return make_response(workout_schema.dump(workout), 200)

    elif request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({"message": f"Workout {id} deleted successfully"}), 200)


# ------------------------------------------------------------------
# EXERCISE ENDPOINTS
# ------------------------------------------------------------------

@app.route('/exercises', methods=['GET', 'POST'])
def handle_exercises():
    if request.method == 'GET':
        exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(exercises), 200)

    elif request.method == 'POST':
        json_data = request.get_json() or {}
        try:
            validated_data = exercise_schema.load(json_data)
            new_exercise = Exercise(**validated_data)
            db.session.add(new_exercise)
            db.session.commit()
            return make_response(exercise_schema.dump(new_exercise), 201)
        except ValidationError as err:
            return make_response(jsonify({"errors": err.messages}), 422)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": [str(e)]}), 400)


@app.route('/exercises/<int:id>', methods=['GET', 'DELETE'])
def handle_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    if request.method == 'GET':
        return make_response(exercise_schema.dump(exercise), 200)

    elif request.method == 'DELETE':
        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({"message": f"Exercise {id} deleted successfully"}), 200)


# ------------------------------------------------------------------
# JOIN TABLE ENDPOINT
# ------------------------------------------------------------------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response(jsonify({"error": "Workout or Exercise not found"}), 404)

    json_data = request.get_json() or {}
    try:
        validated_data = workout_exercise_schema.load(json_data)
        new_we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **validated_data
        )
        db.session.add(new_we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_we), 201)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"errors": [str(e)]}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)