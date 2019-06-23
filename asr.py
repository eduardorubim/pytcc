from __future__ import print_function
from os import path
import speech_recognition
import pyaudio
import time
from playsound import playsound
from pocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path

decoder = None # deixar global ou deixar na classe?
pa = None
sr = None
    
"""
Módulo Automatic Speech Recognition usando API da Google
"""
class ASR:
    def init():
        config = DefaultConfig()
        sr_dir =path.dirname(path.abspath(speech_recognition.__file__))
        client_dir = path.dirname(path.abspath(__file__))
        model_path = path.join(sr_dir, 'pocketsphinx-data')
        #data_path = get_data_path()

        #config.set_string('-logfn', path.join(client_dir,'log/pocketsphinx.log'))
        #config.set_string('-hmm', path.join(model_dir, 'en-US', 'acoustic-model'))
        config.set_string('-hmm', path.join(model_path, 'en-US','acoustic-model')) # (msm sem pt, é só para "Minerva")
        config.set_string('-dict', path.join(model_path, 'en-US', 'pronounciation-dictionary.dict'))
        #config.set_string('-lm', path.join(model_path,  'en-US', 'language-model.lm.bin'))
        #config.set_string('-kws', path.join(client_dir, 'keywords.txt'))
        #config.set_string('-keyphrase', 'minerva')
        #config.set_float('-kws_threshold', 1e+20)

        global decoder, pa
        decoder = Decoder(config)
        decoder.set_kws('keyword', path.join(client_dir, 'keywords.txt'))
        decoder.set_search('keyword')
        pa = pyaudio.PyAudio()

        global sr
        sr = speech_recognition.Recognizer()


    def listen():
        global sr
        with speech_recognition.Microphone() as source:
            sr.adjust_for_ambient_noise(source)
            print("Ouvindo... ")
            playsound("double-beep.mp3")
            audio = sr.listen(source)
            phrase = ''

        try:
            phrase = sr.recognize_google(audio, language='pt-BR')
        except speech_recognition.UnknownValueError:
            print("Não entendi")
        finally:
            return phrase    
    
    def listen_keyword():
        global decoder, pa
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000,
                        input=True, frames_per_buffer=1024)
        stream.start_stream()

        print("Operante e esperando ativação...")
        # Processa chunks de audio
        decoder.start_utt()
        start = time.time()
        while True:
            buf = stream.read(1024, exception_on_overflow=False)
            if buf:
                decoder.process_raw(buf, False, False)
                if decoder.hyp():
                    print(decoder.hyp().hypstr)
                    if "cancel" in decoder.hyp().hypstr:
                        decoder.end_utt()
                        return -1
                    elif "minerva" in decoder.hyp().hypstr:
                        decoder.end_utt()
                        return 1
                    elif (time.time() - start) >= 300:
                        return 0