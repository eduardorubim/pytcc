import os
import json
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account

from src.tts import TTS
from src.asr import ASR
# from dialog_manager import DM

"""
Módulo Cliente Minerva
"""
class Client:
    def __init__(self):
        self.asr = ASR()
        self.tts = TTS()

        # TODO: isso deve ir pra config, preferencialmente num JSON
        self.DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
        self.DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
        self.GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('pytcc/credentials/smart-home-1-6c30f-b1024858ceb7.json')
        self.SESSION_ID = 'tcc-chatbot'

    def run(self):

        session_client = dialogflow.SessionsClient(credentials=self.GOOGLE_APPLICATION_CREDENTIALS)
        session = session_client.session_path(self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)

        while True:

            try:
                self.asr.wait_keyword()
                text_to_be_analyzed = self.asr.listen()

                if not text_to_be_analyzed:
                    print("[Client]Nada reconhecido")
                    continue
                else:
                    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
                    query_input = dialogflow.types.QueryInput(text=text_input)  
                    try:
                        response = session_client.detect_intent(session=session, query_input=query_input)
                    except InvalidArgument:
                        raise
                    
                    """
                    TODO: gerenciador de diálogos espertinho
                    if DM.match_intent(response.query_result.intent.display_name):
                        DM.intent(response.query_result.intent.display_name).execute(response.query_result.parameters)
                    """

                    print("[Client]Query text:", response.query_result.query_text)
                    print("[Client]Detected intent:", response.query_result.intent.display_name)
                    print("[Client]Detected intent confidence:", response.query_result.intent_detection_confidence)
                    print("[Client]Detected parameters:", response.query_result.parameters)
                    print("[Client]Fulfillment text:", response.query_result.fulfillment_text)

                    if response.query_result.fulfillment_text:
                        self.tts.speak(response.query_result.fulfillment_text)
                    else:
                        print("[Client]Não há uma resposta")

            except KeyboardInterrupt:
                print ("\n[Client]Parando cliente")
                break



    