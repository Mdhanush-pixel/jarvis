import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
import os
import google.generativeai as genai

# Setup Gemini API (it looks for GEMINI_API_KEY env var)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Initialize TTS engine
engine = pyttsx3.init()

# Setup logging
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def save_to_log(user_input, response):
    """Saves conversation to a text file in the logs directory."""
    filename = os.path.join(LOG_DIR, f"conv_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt")
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User: {user_input}\n")
        f.write(f"[{timestamp}] Jarvis: {response}\n\n")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def chat_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Sorry, I am having trouble connecting to my brain right now."

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    response = f"The current time is {now}"
    speak(response)
    return response

def tell_date():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    response = f"Today's date is {today}"
    speak(response)
    return response

def open_website(url):
    speak(f"Opening {url}")
    webbrowser.open(url)
    return f"Opened {url}"

if __name__ == "__main__":
    speak("Jarvis initialized. How can I help you?")
    
    while True:
        query = listen()
        
        if query == "none":
            continue
        
        response = ""
        if 'time' in query:
            response = tell_time()
        elif 'date' in query:
            response = tell_date()
        elif 'open google' in query:
            response = open_website("https://www.google.com")
        elif 'stop' in query:
            speak("Goodbye!")
            break
        else:
            # If no command matched, ask Gemini
            speak("Let me think...")
            response = chat_with_gemini(query)
            speak(response)
        
        # Save to log if there was a meaningful interaction
        if response:
            save_to_log(query, response)
