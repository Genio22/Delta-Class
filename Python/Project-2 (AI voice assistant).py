import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
import openai  # Install using: pip install openai

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key_here'

# Function to speak the response
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

# Function to recognize speech input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

# Main loop
while True:
    user_input = listen()
    
    if user_input:
        # Send user input to GPT API for processing
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the GPT model
            prompt=user_input,
            max_tokens=50  # Adjust based on desired response length
        )
        
        # Get GPT response and speak it
        gpt_response = response.choices[0].text.strip()
        speak(gpt_response)
