from flask import Flask, render_template, request
import requests

app = Flask(__name__)



# API ----
EXERCISES_API = "https://wger.de/api/v2/exercise/"
EXERCISE_INFO_API = "https://wger.de/api/v2/exerciseinfo/"

BODY_PARTS = {
    "Shoulders": [13],
    "Arms": [8, 9, 10],
    "Legs": [11, 14, 7],
    "Back": [12],
    "Abdomen": [6],
}

def fetch_exercises(category_ids):
    response = requests.get(EXERCISES_API, params={"language": 2, "limit": 100, "category": ",".join(map(str, category_ids))})
    return response.json().get('results', [])

def fetch_exercise_details(exercise_id):
    response = requests.get(f"{EXERCISE_INFO_API}{exercise_id}", params={"language": 2})
    return response.json()

@app.route('/')
def home():
    return render_template('home.html', body_parts=BODY_PARTS.keys())

@app.route('/exercises/<body_part>')
def exercises(body_part):
    category_ids = BODY_PARTS.get(body_part, [])
    exercises = fetch_exercises(category_ids)
    return render_template('index.html', exercises=exercises, body_part=body_part)

@app.route('/exercise/<int:exercise_id>')
def exercise_details(exercise_id):
    details = fetch_exercise_details(exercise_id)
    return render_template('exercise.html', details=details)

if __name__ == '__main__':
    app.run(debug=True)
