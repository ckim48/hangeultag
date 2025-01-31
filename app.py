from flask import Flask, render_template, request, jsonify,session
import serial
import threading
import csv
import time
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

import csv

def generate_problem_set_from_csv(csv_file):
    problem_set = {}

    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if it exists

        for row in csv_reader:
            category, korean_name, english_name, level = row[:4]
            level = int(level)

            # Extract correct answer from columns 1-9 (zero-based index: 4 to 12)
            correct_answer = ",".join(row[4:13]).strip()  # Ensure it's properly formatted

            # Build problem set
            if category not in problem_set:
                problem_set[category] = {}

            if level not in problem_set[category]:
                problem_set[category][level] = []

            problem_set[category][level].append({
                "question": f"What is the English name of '{korean_name}'?",
                "english_name": english_name,
                "answer": correct_answer  # Store the correct answer
            })

    return problem_set



problem_set = generate_problem_set_from_csv('datafile.csv')


arduino_data = []

SERIAL_PORT = "COM3"
BAUD_RATE = 115200
@app.route('/check_answer', methods=['POST'])
def check_answer():
    category = request.json.get('category')
    level = int(request.json.get('level'))
    user_answer = request.json.get('answer').strip().lower()

    # Validate inputs
    if category not in problem_set or level not in problem_set[category]:
        return jsonify({'correct': False, 'message': 'Invalid category or level.'})

    problems = problem_set[category][level]
    total_questions = len(problems)

    # Convert (category, level) to a session key
    session_key = f"{category}_{level}"

    # Store last played category and level for review filtering
    session['last_played'] = session_key

    # Retrieve the current question index from session
    if 'question_index' not in session or session_key not in session['question_index']:
        return jsonify({'correct': False, 'message': 'Question index not initialized.'})

    current_index = session['question_index'][session_key] - 1

    if current_index < 0 or current_index >= total_questions:
        return jsonify({'correct': False, 'message': 'Invalid question index.'})

    # Get question and correct answer
    problem = problems[current_index]
    korean_name = problem["question"].split("'")[1]
    english_name = problem["english_name"]
    correct_answer_str = problem["answer"]

    # Normalize answers
    correct_answer_str = "".join([char.strip().lower() for char in correct_answer_str.split(',') if char.strip()])
    user_answer_str = "".join([char.strip().lower() for char in user_answer.split(',') if char.strip()])

    # Compare user answer
    is_correct = user_answer_str == correct_answer_str

    # Initialize tracking if not already done
    if 'correct_count' not in session:
        session['correct_count'] = 0
        session['incorrect_count'] = 0

    # Update correct/incorrect counts
    if is_correct:
        session['correct_count'] += 1
    else:
        session['incorrect_count'] += 1

    # Store review data with session key
    if 'review_data' not in session:
        session['review_data'] = []

    session['review_data'].append({
        "session_key": session_key,  # ✅ Add session key to track category & level
        "korean_name": korean_name,
        "english_name": english_name,
        "user_answer": user_answer_str,
        "correct_answer": correct_answer_str,
        "is_correct": is_correct
    })

    # Check if this was the last question
    if current_index + 1 >= total_questions:
        return jsonify({'redirect': True, 'url': '/result'})

    return jsonify({'correct': is_correct, 'redirect': False})


@app.route('/result')
def result():
    correct_count = session.get('correct_count', 0)
    incorrect_count = session.get('incorrect_count', 0)
    review_data = session.get('review_data', [])

    # Get the last played category and level from session
    last_session_key = session.get('last_played', None)

    # Filter review data to only show for the last played category & level
    if last_session_key:
        category, level = last_session_key.split("_")
        filtered_review_data = [review for review in review_data if f"{category}_{level}" in review.get("session_key", "")]
    else:
        filtered_review_data = []

    # Clear session variables for a new game
    session.pop('correct_count', None)
    session.pop('incorrect_count', None)

    # ✅ Ensure question index is removed so new games start fresh
    session.pop('question_index', None)
    session.pop('review_data', None)  # Clears review data after displaying it
    session.modified = True  # Ensure session changes are saved

    return render_template(
        'result.html',
        correct_count=correct_count,
        incorrect_count=incorrect_count,
        review_data=filtered_review_data  # Pass filtered review data
    )

def read_from_arduino():
    global arduino_data
    fake_words = ["ㅇ,ㅐ,ㅇ,ㅁ,,ㅜ,ㅅ,ㅐ,,","ㅇ,ㅛ,ㅇ,,,,,,,"]

    while True:
        simulated_data = random.choice(fake_words)  # Pick a random word
        print(f"Simulated Arduino Data: {simulated_data}")  # Simulate print like Arduino
        arduino_data.append(simulated_data)  # Append to list
        time.sleep(3)  # Simulate delay like serial read

# def read_from_arduino():
#     global arduino_data
#     try:
#         with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
#             while True:
#                 if ser.in_waiting > 0:
#                     try:
#                         line = ser.readline().decode('utf-8').strip()
#                         if line:
#                             print(f"Arduino Data: {line}")
#                             threading.Lock().acquire()  # Lock to ensure thread safety
#                             arduino_data.append(line)  # Append new data
#                             threading.Lock().release()  # Release the lock
#                     except UnicodeDecodeError as e:
#                         print(f"Error decoding data: {e}")
#     except serial.SerialException as e:
#         print(f"Serial error: {e}")


# thread = threading.Thread(target=read_from_arduino, daemon=True)
# thread.start()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def get_data():
    global arduino_data
    if not arduino_data:
        return jsonify({"error": "No data received yet"}), 400
    print({"arduino_data": arduino_data[-1]})
    return jsonify({"arduino_data": arduino_data[-1]})  # Send only the latest data


import os


import os
import unicodedata

def normalize_string(s):
    return unicodedata.normalize('NFC', s).strip()
def find_audio(korean_name):
    static_folder = "static/Audios/"
    korean_name = normalize_string(korean_name)  # Normalize input string


    for root, _, files in os.walk(static_folder):
        for file in files:
            normalized_file = normalize_string(file)


            if korean_name in normalized_file:
                return os.path.join(root, file).replace("\\", "/")  # Return web-compatible path

    return None  # Return None if no file is found

def find_image(korean_name):
    static_folder = "static/images/"
    korean_name = normalize_string(korean_name)  # Normalize input string


    for root, _, files in os.walk(static_folder):
        for file in files:
            normalized_file = normalize_string(file)


            if korean_name in normalized_file:
                return os.path.join(root, file).replace("\\", "/")  # Return web-compatible path

    return None  # Return None if no file is found
@app.route('/game')
def game():
    category = request.args.get('category')
    level = int(request.args.get('level'))

    # Validate category and level
    if category not in problem_set or level not in problem_set[category]:
        return "Invalid category or level."

    problems = problem_set[category][level]
    total_questions = len(problems)

    # Convert (category, level) to a session key
    session_key = f"{category}_{level}"

    # Ensure `session['question_index']` exists and is a dictionary
    if 'question_index' not in session:
        session['question_index'] = {}

    # If category-level pair is not in session, initialize at 0
    if session_key not in session['question_index']:
        session['question_index'][session_key] = 0

    current_index = session['question_index'][session_key]

    # Ensure index does not exceed total questions
    if current_index >= total_questions:
        session['question_index'][session_key] = 0  # Restart after completion

    # Fetch current problem
    current_problem = problems[current_index]

    # Extract Korean name from the problem
    korean_name = current_problem["question"].split("'")[1]

    # Find corresponding image and audio
    image_path = find_image(korean_name)
    audio_path = find_audio(korean_name)

    # Get correct answer
    correct_answer = current_problem["answer"]

    # ✅ Persistently update session
    session['question_index'][session_key] += 1
    session.modified = True  # 🚀 Force session to save changes

    # print(f"Category: {category}, Level: {level}, Question {current_index + 1}/{total_questions}")
    # print(f"Correct Answer: {correct_answer}")
    # print(f"Audio Path: {audio_path}")

    return render_template(
        'gamepage.html',
        category=category,
        level=level,
        korean_name=korean_name,
        english_name=current_problem.get("english_name", "No English Name"),
        correct_answer=correct_answer,
        question_number=current_index + 1,
        total_questions=total_questions,
        image_path=image_path,
        audio_path=audio_path
    )



if __name__ == "__main__":
    thread = threading.Thread(target=read_from_arduino, daemon=True)
    thread.start()
    app.run(debug=True, port=8080)