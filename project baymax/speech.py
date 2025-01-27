import speech_recognition as sr
from gtts import gTTS
from translate import Translator
import os
import win32gui
import win32con
import time

r = sr.Recognizer()

def listen(language):
    translator = Translator(to_lang=language)
    while True:
        with sr.Microphone() as source:
            print("Listening")
            audio_text = r.listen(source)
            try:
                return translator.translate(r.recognize_google(audio_text))
            except Exception:
                d_not = translator.translate("Sorry i didn't understand you")
                didn_id = gTTS(text=d_not, lang=language, slow=False)
                didn_id.save("didn_id.mp3")
                os.system(f"start didn_id.mp3")
                Minimize = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(Minimize, win32con.SW_HIDE)
                time.sleep(2)
                os.remove(f"didn_id.mp3")
