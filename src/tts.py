from gtts import gTTS
from playsound import playsound

"""
Módulo Text-to-Speech usando gTTs
"""
class TTS:

    def __init__(self):
        pass

    def speak(self, text_to_speak):
        tts = gTTS(text=text_to_speak, lang='pt-br')
        tts.save("audio/say.mp3")
        playsound("audio/say.mp3")