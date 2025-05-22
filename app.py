from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_assets import Environment, Bundle
from werkzeug.utils import secure_filename
import os
from deepface import DeepFace
import random

# Import custom modules
from youtube_api import get_youtube_videos
from mood_model import detect_emotion_1
from emotion_map import emotion_content_map

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'moodify'
mysql = MySQL(app)

# Configure upload folder for images
app.config['UPLOAD_FOLDER'] = 'static/images'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Flask-Assets
assets = Environment(app)
scss_bundle = Bundle('scss/main.scss', filters='libsass', output='css/main.css')
assets.register('scss_all', scss_bundle)

# -------------------- Routes --------------------

@app.route('/')
def home():
    """First page the user sees when the app is run."""
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login. Redirects to main.html after successful login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            session['firstname'] = user['firstname']
            return redirect(url_for('main_page'))
        return "Invalid credentials!"

    return render_template('login.html')

@app.route('/main')
def main_page():
    """Displays the main dashboard where users can detect mood."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    return render_template(
        'main.html',
        mood=None,
        music_videos_lang={},
        movie=None,
        youtube_videos=[],
        firstname=session.get('firstname')
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    """Registers a new user and redirects to login."""
    fname = request.form['firstname']
    lname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']

    if not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.(com)$', email):
        return "Invalid email", 400
    if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$', password):
        return "Weak password", 400

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()

    if account:
        return "Account already exists!"
    else:
        cursor.execute('INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)',
                       (fname, lname, email, password))
        mysql.connection.commit()
        return redirect(url_for('login'))  # Redirect to login after registration

@app.route('/detect-mood', methods=['POST'])
def detect_mood_text():
    """Detects mood from text input."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    user_text = request.form.get("text")
    if not user_text:
        return jsonify({"error": "Text input missing!"}), 400

    mood = detect_emotion_1(user_text).lower()
    data = generate_recommendations(mood)
    return render_template('main.html', **data)

@app.route('/detect-mood-from-face', methods=['POST'])
def detect_mood_from_face():
    """Detects mood using face recognition."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if 'image' not in request.files:
        return "No file found", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        analysis = DeepFace.analyze(img_path=filepath, actions=['emotion'], enforce_detection=False)
        mood = analysis[0]['dominant_emotion'].lower()
    except Exception as e:
        return f"Face detection error: {e}", 500

    data = generate_recommendations(mood)
    return render_template('main.html', **data)

def generate_recommendations(mood):
    """Fetches recommendations based on mood."""
    suggestions = emotion_content_map.get(mood, {
        "music_query": "relaxing music",
        "movie_genre": "drama",
        "youtube_query": "motivational talks"
    })

    languages = ["English", "Telugu", "Tamil", "Malayalam", "Hindi", "Marathi"]
    music_videos_lang = {}
    unique_video_ids = set()

    for lang in languages:
        query = f"{suggestions['music_query']} in {lang}"
        videos = get_youtube_videos(query)
        filtered_videos = [video for video in videos if video["url"] not in unique_video_ids]
        unique_video_ids.update(video["url"] for video in filtered_videos)
        random.shuffle(filtered_videos)
        music_videos_lang[lang] = filtered_videos[:5]

    youtube_videos = get_youtube_videos(suggestions["youtube_query"])

    return {
        "mood": mood.title(),
        "music_videos_lang": music_videos_lang,
        "movie": suggestions["movie_genre"],
        "youtube_videos": youtube_videos
    }

if __name__ == '__main__':
    app.run(debug=True)
