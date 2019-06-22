from __future__ import print_function
from os import path
import speech_recognition
import pyaudio
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
        sr_dir = path.dirname(path.abspath(sr.__file__))
        client_dir = path.dirname(path.abspath(__file__))
        model_dir = path.join(sr_dir, 'pocketsphinx-data')
        model_path = get_model_path()
        #data_path = get_data_path()

        config.set_string('-logfn', path.joing(client_dir,'log/pocketsphinx.log'))
        #config.set_string('-hmm', path.join(model_dir, 'en-US', 'acoustic-model'))
        config.set_string('-hmm', path.join(model_path, 'en-us')) # (msm sem pt, é só para "Minerva")
        config.set_string('-dict', path.join(model_path, 'cmudict-en-us.dict'))
        #config.set_string('-lm',    path.join(model_dir,  'en-US', 'language-model.lm.bin'))
        config.set_string('-kws',   path.join(client_dir, 'keyphrases.txt'))

        global decoder, pa
        decoder = Decoder(config)
        pa = pyaudio.PyAudio()

        global sr
        sr = speech_recognition.Recognizer()


    def listen():
        mp = sr.Recognizer()
        with sr.Microphone() as source:
            mp.adjust_for_ambient_noise(source)
            print("Ouvindo... ")
            playsound("double-beep.mp3")
            audio = mp.listen(source)
            phrase = ''

        try:
            phrase = mp.recognize_google(audio, language='pt-BR')
        except sr.UnknownValueError:
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
        waiting = False
        wait_count = 0
        while True:
            buf = stream.read(1024, exception_on_overflow=False)
            decoder.process_raw(buf, False, False)
            if decoder.hyp():
                if decoder.hyp().hypstr[:13] == "minerva cancel" or decoder.hyp().hypstr[:11] == "minerva cancela":
                    decoder.end_utt()
                    return "minerva cancel"
                else:
                    if waiting:
                        if wait_count >= 8:
                            decoder.end_utt()
                            return "minerva"
                        else:
                            wait_count += 1
                    else:
                        waiting = True
