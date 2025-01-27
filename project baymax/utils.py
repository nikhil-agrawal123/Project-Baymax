import re

def load_symptoms(file_path):
    with open(file_path, 'r') as f:
        symptoms = [line.strip().lower() for line in f if line.strip()]
    return symptoms

def detect_symptoms(text, symptom_list):
    input_line = text.lower()
    detected_symptoms = [symptoms for symptoms in symptom_list if re.search(r'\b' + re.escape(symptoms) + r'\b', input_line)]
    return detected_symptoms
