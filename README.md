# 🎵 Moodify

**Moodify** is an intelligent music recommendation system that curates playlists based on your current mood. By leveraging facial emotion recognition and integrating with the YouTube API, Moodify delivers a personalized musical experience tailored to your emotions.

---

**Note : Please use Python 3.10.12 before downloading the requirments or you will get an error**

## 📌 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- **Facial Emotion Detection**: Utilizes computer vision to detect user emotions in real-time.
- **Mood-Based Music Recommendations**: Maps detected emotions to appropriate music genres.
- **YouTube Integration**: Fetches and plays songs from YouTube based on the user's mood.
- **User-Friendly Interface**: Interactive and responsive UI for seamless user experience.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python, Flask
- **Libraries**:
  - OpenCV (cv2)
  - TensorFlow
  - Keras
  - Requests
  - NumPy
- **APIs**:
  - YouTube Data API

---

## ⚙️ Installation

Follow these steps to set up and run Moodify on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/shawnie117/Moodify.git
cd Moodify
```


## **Step 2: Create a virtual environment**

- **For Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

- **For macOS/Linux :**
```bash
python -m venv venv
source venv/bin/activate
```


## **Step 3: Install dependencies**
#### Install the required dependencies listed in requirements.txt :
```bash
pip install -r requirements.txt
```


## **Step 4: Run the application**
#### Start the Flask server :
```bash
python app.py
```

#### Then, open http://127.0.0.1:5000/ in your browser to access the dashboard.

# File Structure 📂

```bash
Moodify/
├── static/
│   ├── css/
│   │   ├── home.css
│   │   ├── main.css
│   │   └── style.css
│   └── images/
│       └── bg.png
├── templates/
│   ├── home.html
│   ├── login.html
│   └── main.html
├── .cache/
├── .gitignore
├── app.py
├── emotion_map.py
├── face_model.py
├── mood_model.py
├── youtube_api.py
├── requirements.txt
└── README.md
```


- `static/css/`: Contains all CSS files for styling different views.
- `static/images/`: Contains background image used in the UI.
- `templates/`: All HTML pages rendered by Flask (login, home, and main interface).
- `.cache/`: Temporary files (can be ignored or added to `.gitignore`).
- `app.py`: Core Flask application logic.
- `emotion_map.py`: Maps detected emotions to relevant music genres.
- `face_model.py`: Handles webcam and facial emotion detection.
- `mood_model.py`: Manages mood interpretation and logic.
- `youtube_api.py`: Handles music search and fetching from YouTube.
- `requirements.txt`: Lists all Python dependencies.
- `README.md`: You’re reading it now 😄




# Bash Scripts 📜
### **Start the Flask server :**

- **For Windows :**
```bash
venv\Scripts\activate
python app.py
```

- **For macOS/Linux :**
```bash
source venv/bin/activate
python app.py
```


### Deactivate the virtual environment

```bash
deactivate
```


# Contributing 🤝

**Contributions are welcome! Feel free to fork this repository, submit issues, or create pull requests.**

# License 📜
**This project is licensed under the MIT License.**