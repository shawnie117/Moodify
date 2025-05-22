import google.generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyBXkDsjo3n22bf35YLvjmbBC2c6yHhRd9o")

candidate_labels = [
    "happiness", "elation", "contentment", "bliss", "amusement", "delight", "cheerfulness",
    "enthusiasm", "optimism", "sorrow", "grief", "unhappiness", "melancholy", "despair",
    "disappointment", "loneliness", "hopelessness", "fury", "rage", "irritation", "frustration",
    "hostility", "annoyance", "resentment", "bitterness", "terror", "fright", "apprehension",
    "anxiety", "nervousness", "worry", "dread", "panic", "revulsion", "contempt", "distaste",
    "aversion", "loathing", "repulsion", "astonishment", "amazement", "wonder", "shock",
    "bewilderment", "sexual desire", "craving", "longing", "self-assurance", "belief", "poise",
    "assurance", "shame", "guilt", "remorse", "embarrassment", "humiliation", "triumph",
    "accomplishment", "self-esteem", "superiority", "self-consciousness", "awkwardness",
    "discomfiture", "affection", "intimacy", "fondness", "care", "compassion", "devotion",
    "passion", "infatuation", "desire", "tenderness", "indifference", "apathy", "calmness",
    "placidity", "jealousy", "envy", "possessiveness", "suspicion", "empathy", "understanding",
    "sympathy", "dissatisfaction", "impatience", "hope", "expectation", "anticipation", "unease",
    "boredom", "lack of interest", "monotony", "uncertainty", "disorientation", "gratitude",
    "thankfulness", "appreciation", "awe", "reverence"
]

def detect_emotion_1(text):
    """
    Detect emotion from text using Gemini API and zero-shot classification.
    """
    if not text or not text.strip():
        return "neutral"
    
    prompt = f"""
Given the following text, determine the most appropriate emotional label from the list.

Text: "{text}"

Emotion Labels: {", ".join(candidate_labels)}

Respond with the single most relevant emotion label only.
"""
    try:
        response = genai.GenerativeModel(model_name="gemini-1.5-flash").generate_content(prompt)
        result = response.text.strip().lower()
        return result
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    text_input = "I'm extremely happy today because I achieved my goals."
    print("Detected emotion:", detect_emotion_1(text_input))
