from gtts import gTTS
from playsound import playsound

buf_count = 0 # usamos dois arquivos de audio intercalados como buffer (cheque gtts-unable-to-save-file-twice)

"""
Módulo Text-to-Speech usando gTTs
"""
class TTS:
    def speak(text_to_speak):
        global buf_count

        tts = gTTS(text=text_to_speak, lang='pt-br')
        tts.save(f'say{buf_count%2}.mp3')
        playsound(f'say{buf_count%2}.mp3')
        buf_count += 1

# TTS.speak("Isso é um teste.")