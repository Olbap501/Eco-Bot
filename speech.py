import pyttsx3

engine = pyttsx3.init()

def read(text):
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 0.9)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(text)
    engine.runAndWait()