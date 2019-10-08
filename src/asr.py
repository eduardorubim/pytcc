import speech_recognition as sr
from porcupine.binding.python.porcupine import Porcupine
import pyaudio
import struct
from playsound import playsound
import platform

"""
Módulo Automatic Speech Recognition usando API da Google
"""
class ASR:
    def __init__(self):
        os = platform.system()
        if (os == 'Darwin'):
            self._library_path = 'porcupine/lib/mac/x86_64/libpv_porcupine.dylib'
            #self._keyword_file_path = 'keyword/minerva_mac.ppn'
            self._keyword_file_path = 'porcupine/resources/keyword_files/mac/alexa_mac.ppn'
        elif (os == 'Windows'):
            self._library_path = 'porcupine/lib/windows/amd64/libpv_porcupine.dll'
            #self._keyword_file_path = 'keyword/minerva_windows.ppn'
            self._keyword_file_path = 'porcupine/resources/keyword_files/windows/alexa_windows.ppn'
        elif (os == 'Linux'):
            self._library_path = 'porcupine/lib/linux/x86_64/libv_porcupine.so'
            #self._keyword_file_path = 'keyword/minerva_linux.ppn'
            self._keyword_file_path = 'porcupine/resources/keyword_files/linux/alexa_linux.ppn'
        self._model_file_path = 'porcupine/lib/common/porcupine_params.pv'
        self._sensitivity = 0.7
        self._input_device_index = None

# Ouve uma frase, retorna o texto
    def listen(self):
        mp = sr.Recognizer()
        phrase = None
        with sr.Microphone() as source:
            #mp.adjust_for_ambient_noise(source)
            #playsound("pytcc/audio/double-beep.mp3")
            print("[ASR] Ouvindo")
            try:
                audio = mp.listen(source)
                try:
                    phrase = mp.recognize_google(audio, language='pt-BR')
                except sr.UnknownValueError:
                    print ("[ASR] Não Entendi")
            finally:
                return phrase

# Espera keyword
    def waitKeyword(self):
        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = Porcupine(
                library_path=self._library_path,
                model_file_path=self._model_file_path,
                keyword_file_path=self._keyword_file_path,
                sensitivity=self._sensitivity)
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=self._input_device_index)

            print("[ASR] Esperando keyword")
            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                result = porcupine.process(pcm)
                if result:
                    print("[ASR] Keyword detectada")
                    break
        finally:
            #print ("\n[ASR]Limpando...")
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()