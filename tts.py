from gtts import gTTS
from playsound import playsound

"""
Módulo Text-to-Speech usando gTTs
"""
class TTS:
    def speak(text_to_speak):
        tts = gTTS(text=text_to_speak, lang='pt-br')
        tts.save("say.mp3")
        playsound("say.mp3")

# TTS.speak("Isso é um teste.")