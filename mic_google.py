import speech_recognition as sr

print(1)

r = sr.Recognizer()

with sr.Microphone() as source:
    audio = r.listen(source)

print(1)
try:
# for testing purposes, we're just using the default API key
# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
# instead of `r.recognize_google(audio)`
    text_from_speech = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said " + text_from_speech)
    #process_text(text_from_speech)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

