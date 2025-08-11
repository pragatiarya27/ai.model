import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import threading

# Initialize the speech recognizer and text-to-speech engine
speech_recognizer = sr.Recognizer()
text_to_speech_engine = pyttsx3.init()

speech_lock = threading.Lock()

def convert_text_to_speech(text):
    # """Convert text to speech using a thread-safe mechanism."""
    with speech_lock:
        text_to_speech_engine.say(text)
        text_to_speech_engine.runAndWait()

def capture_audio():
    # """Capture audio from the microphone and return the recognized text."""
    with sr.Microphone() as source:
        print("Listening...")
        speech_recognizer.adjust_for_ambient_noise(source)
        audio = speech_recognizer.listen(source)

        try:
            print("Recognizing...")
            recognized_text = speech_recognizer.recognize_google(audio)
            print(f"You said: {recognized_text}")
            return recognized_text.lower()
        except sr.UnknownValueError:
            convert_text_to_speech("Sorry, I did not understand that. Can you please repeat?")
            return None
        except sr.RequestError:
            convert_text_to_speech("Sorry, I'm having trouble connecting to the speech service.")
            return None

def wait_for_activation_word():
    # """Continuously listen for the activation word to start the assistant."""
    while True:
        print("Say 'hello' to activate...")
        recognized_command = capture_audio()
        if recognized_command and "hello" in recognized_command:
            convert_text_to_speech("Yes, I'm listening")
            break

def process_command(command):
    # """Process the recognized command and perform the corresponding action."""
    if "hello" in command:
        greet_user()
    elif "your name" in command:
        convert_text_to_speech("I am Zora,,,your virtual assistant.")
    elif "time" in command:
        threading.Thread(target=provide_current_time).start()
    elif "date" in command:
        threading.Thread(target=provide_current_date).start()
    elif "open notepad" in command:
        threading.Thread(target=open_notepad_application).start()
    elif "search for" in command:
        threading.Thread(target=perform_web_search, args=(command,)).start()
    elif "remind me to" in command:
        threading.Thread(target=create_reminder, args=(command,)).start()
    elif "exit" in command or "stop" in command:
        convert_text_to_speech("Goodbye!")
        return False
    else:
        ask_for_clarification()
    return True

def greet_user():
    # """Greet the user."""
    convert_text_to_speech("Hello! i am Zora, How can I assist you today?")

def provide_current_time():
    # """Provide the current time to the user."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    convert_text_to_speech(f"The current time is {current_time}")

def provide_current_date():
    # """Provide the current date to the user."""
    current_date = datetime.date.today().strftime("%B %d, %Y")
    convert_text_to_speech(f"Today's date is {current_date}")

def open_notepad_application():
    # """Open Notepad on the user's system."""
    os.startfile("notepad.exe")
    convert_text_to_speech("Opening Notepad")

def perform_web_search(command):
    # """Perform a web search based on the user's command."""
    query = command.replace("search for", "").strip()
    webbrowser.open(f"https://www.google.com/search?q={query}")
    convert_text_to_speech(f"Here are the results for {query}")

def create_reminder(command):
    # """Create a reminder based on the user's command."""
    reminder_text = command.replace("remind me to", "").strip()
    convert_text_to_speech(f"Setting a reminder for: {reminder_text}")
    threading.Thread(target=delay_reminder, args=(reminder_text,)).start()

def delay_reminder(reminder_text):
    # """Delay the reminder and notify the user."""
    time.sleep(10)  # Simple delay (10 seconds for testing)
    convert_text_to_speech(f"Reminder: {reminder_text}")

def ask_for_clarification():
    # """Ask the user for clarification if the command is not understood."""
    convert_text_to_speech("I'm sorry, I didn't catch that. Can you please clarify what you need?")

def run_virtual_assistant():
    # """Run the virtual assistant."""
    while True:
        wait_for_activation_word()
        while True:
            command = capture_audio()
            if command:
                if not process_command(command):
                    break

if __name__ == "__main__":
    run_virtual_assistant()
