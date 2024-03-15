import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

# Set up OpenAI API key and model
openai.api_key = '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'
model = 'gpt-3.5-turbo'

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Configure the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Greetings for wake word detection
name = "Ahnaf"
greetings = [
    f"Hey, what's up, Master {name}?",
    "Yeah?",
    f"Hello, Master {name}! How are you today?",
    f"Greetings, Captain {name}! How's everything?",
    f"Bonjour, Monsieur {name}! Comment ça va?"
]

def listen_for_wake_word(source):
    print("Listening for 'Hey'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "Hello" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue
            # Send input to OpenAI API
            response = openai.Completion.create(
                engine=model,
                prompt=text,
                max_tokens=150
            )
            response_text = response.choices[0].text.strip()
            print(response_text)
            # Speak the response
            engine.say(response_text)
            engine.runAndWait()
            listen_for_wake_word(source)
            break
        except sr.UnknownValueError:
            print("Silence found, listening...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
