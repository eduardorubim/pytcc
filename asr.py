import speech_recognition as sr

"""
Módulo Automatic Speech Recognition usando API da Google
"""
class ASR:
    def listen():
        mp = sr.Recognizer()
        with sr.Microphone() as source:
            mp.adjust_for_ambient_noise(source)
            print("Ouvindo... ")
            audio = mp.listen(source)

        try:
            phrase = mp.recognize_google(audio, language='pt-BR')
        except sr.UnknownValueError:
            return "Não entendi"

        return phrase

#print(ASR.listen())