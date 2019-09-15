import os
import json
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account

from src.tts import TTS
from src.asr import ASR
from src.dm  import DialogManager as DM

"""
Módulo Cliente Minerva
"""
class Client:
    def __init__(self):
        self.asr = ASR()
        self.tts = TTS()
        self.dm = DM()

        # TODO: isso deve ir pra config, preferencialmente num JSON
        self.DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
        self.DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
        self.GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('pytcc/credentials/smart-home-1-6c30f-e78ffd0ca7a1.json')
        self.SESSION_ID = 'tcc-chatbot'

    def run(self):

        session_client = dialogflow.SessionsClient(credentials=self.GOOGLE_APPLICATION_CREDENTIALS)
        session = session_client.session_path(self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)

        while True:

            try:
                self.asr.waitKeyword()
                text_to_be_analyzed = self.asr.listen()

                if not text_to_be_analyzed:
                    print("[Client]Nada reconhecido")
                    continue
                else:
                    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
                    query_input = dialogflow.types.QueryInput(text=text_input)  
                    try:
                        result = session_client.detect_intent(session=session, query_input=query_input)
                    except InvalidArgument:
                        raise
                    
                    response = self.dm.treatResult(result)

                    # Aqui ocorreria o acionamento utilizando:
                    # response[0]   : intent
                    # response[1][ ]: paramenters

                    if response[2]:
                        self.tts.speak(response[2])
                    else:
                        print("[Client]Não há uma resposta")

            except KeyboardInterrupt:
                print ("\n[Client]Parando cliente")
                break



    