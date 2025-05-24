import speech_recognition as sr
import pyttsx3
from nlu import parse_command
from automation import execute_plan

recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text):
    print(f"[TTS] {text}")
    tts.say(text)
    tts.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Say your command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"[Voice] You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        speak(f"Could not request results; {e}")
        return None

def main():
    speak("AI Web Automation Agent. Say your command after the beep. Say 'exit' to quit.")
    while True:
        command = listen()
        if not command:
            continue
        if command.strip().lower() == 'exit':
            speak("Goodbye!")
            break
        plan = parse_command(command)
        speak(f"Parsed: {plan}")
        try:
            execute_plan(plan)
        except Exception as e:
            speak(f"Error: {e}")

if __name__ == "__main__":
    main()

# To use this script, install dependencies:
# pip install SpeechRecognition pyttsx3 pyaudio
# (On Windows, you may need to install PyAudio wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) 