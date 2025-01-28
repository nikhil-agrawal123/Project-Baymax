import pyttsx3
from gtts import gTTS
import os
import time
import win32gui
import win32con
import spacy
import pandas as pd
import speech_recognition as sr
from utils import load_symptoms, detect_symptoms
from database import new_id, has_id
from googletrans import Translator
from bson.objectid import ObjectId

translator = Translator()

all_symptoms = load_symptoms("symptoms.txt")
nlp = spacy.load("en_core_web_sm")
r = sr.Recognizer()
engine = pyttsx3.init()

def speak_and_listen(prompt, language="en"):
    translated_prompt = translator.translate(prompt, src="en",dest=language).text
    tts = gTTS(text=translated_prompt, lang=language, slow=False)
    filename = "temp.mp3"
    tts.save(filename)
    os.system(f"start {filename}")
    time.sleep(3)
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_HIDE)
    os.remove(filename)

    with sr.Microphone() as source:
        print(prompt)
        try:
            audio = r.listen(source)
            response = r.recognize_google(audio, language=language)
            return response
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None


def get_user_details(language):
    name = speak_and_listen("What is your name?", language)
    doc = nlp(str(translator.translate(name, src=language, dest="en")))
    for token in doc.ents:
        if token.label_ == "PERSON":
            name = token.text
    print(name)
    gender = speak_and_listen("What is your gender?", language)
    while True:
        if not gender:
            gender = speak_and_listen("Sorry i didn't get that please say that again", language)
        else:
            gender = gender.lower()
            if gender == "mail":
                gender = "male"
            break

    max_attempts = 3
    attempts = 0
    age = 0

    while (age == 0 ) and attempts < max_attempts:
        age = speak_and_listen("What is your age?", language)
        doc = nlp(str(translator.translate(gender, src=language, dest="en")))

        for token in doc.ents:
            if token.label_ in {"DATE", "CARDINAL"} and age == 0:
                age = token.text

        if age == 0:
            age = speak_and_listen("Sorry, I didn't get that. Please say again.", language)
            attempts += 1
        else:
            break

    if age == 0 :
        print("Failed to capture age and weight accurately.")

    severity = speak_and_listen("On a scale of 1 to 10 what is the severity of the symptoms?", language)

    return name, gender, age, severity

def read_symptom_detail(file_path,symptoms):
    file = pd.read_csv(file_path)
    category = [row['Main Category'] for _,row in file.iterrows() if row['Symptoms'] in symptoms]
    category = set(category)
    return category

def main():
    language = input("English or हिंदी: ").strip().lower()
    language = "hi" if language == "हिंदी" else "en"

    name, gender, age, severity = get_user_details(language)

    symptoms = speak_and_listen("What are your symptoms?", language)
    detected_symptoms = detect_symptoms(symptoms, all_symptoms)
    print(f"Detected Symptoms: {detected_symptoms}" if detected_symptoms else "No symptoms detected.")
    print(read_symptom_detail("sorted_main_categories.csv", detected_symptoms))
    duration = speak_and_listen("How long have you been experiencing these symptoms?", language)
    print(duration)

    try:
        has_visited = speak_and_listen("Have you visited us before? (yes or no)", language)
        if str(has_visited) == "yes":
            user_id = input("Enter your user ID: ")
            has_id(ObjectId(user_id), name, gender, age, detected_symptoms,duration,severity)
        else:
            new_id(name, age, gender, detected_symptoms,duration,severity)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()