from __future__ import print_function
import traceback
import os
import re
import json
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account

from tts import TTS
from asr import ASR
# from dialog_manager import DM

inst = None

try:
    input = raw_input  # Python 2 fix
except NameError:
    pass

def init():
    global inst
    inst = CLIENT()

"""
Módulo Cliente Minerva
"""
class CLIENT:
    def __init__(self,greet_user=True):
        #self.api = api.init() TODO: vale a pena?
        ASR.init()
        #TTS.init()

        self.key_word = "minerva"
        if greet_user:
            self.greet()        
        
        self.quit_flag = False

        # TODO: isso deve ir pra config, preferencialmente num JSON
        self.DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
        self.DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
        self.GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('credentials/smart-home-1-6c30f-b1024858ceb7.json')
        self.SESSION_ID = 'tcc-chatbot'
        
        self.session_client = dialogflow.SessionsClient(credentials=self.GOOGLE_APPLICATION_CREDENTIALS)
        self.session = self.session_client.session_path(self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)
     
         
    def greet(self):
        print("Olá, eu atendo por " + self.key_word.title())
        print("Tente comandos como:")
        print(self.key_word.title() + " (beep) apague a luz da sala;")
        print(self.key_word.title() + " (beep) configure uma rotina.")
        TTS.speak("Olá, eu atendo por " + self.key_word.title())
        #TTS.speak("Me chame. então espere pelo beep de ativação")

    def run(self):
        while True:
            if self.quit_flag:
                break

            check = ASR.listen_keyword()
            if check == -1:
                self.quit_flag = True;
                continue
            if check == 0:
                continue
            if check == 1:
                text_to_be_analyzed = ASR.listen()

                if not text_to_be_analyzed:
                    print("nada reconhecido")
                    continue
                else:
                    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
                    query_input = dialogflow.types.QueryInput(text=text_input)  
                    try:
                        response = self.session_client.detect_intent(session=self.session, query_input=query_input)
                    except InvalidArgument:
                        raise
                
                    """
                    TODO: gerenciador de diálogos espertinho
                    if DM.match_intent(response.query_result.intent.display_name):
                        DM.intent(response.query_result.intent.display_name).execute(response.query_result.parameters)
                    """

                    print("Query text:", response.query_result.query_text)
                    print("Detected intent:", response.query_result.intent.display_name)
                    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
                    print("Detected parameters", response.query_result.parameters)
                    print("Fulfillment text:", response.query_result.fulfillment_text)

                    TTS.speak(response.query_result.fulfillment_text)



    