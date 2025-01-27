from googletrans import Translator

translator = Translator()
translated_text = translator.translate("मुझे पिछले कुछ दिनों से सिरदर्द और उल्टी हो रही है", src="hi", dest="en")
print(translated_text.text)
