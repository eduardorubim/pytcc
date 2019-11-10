import os
import json
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

from src.tts import TTS
from src.asr import ASR
from src.dm  import DialogManager as DM
from src.globals import *

"""
Módulo Cliente Minerva
"""
class Client:
    def __init__(self, sim_stdin):
        self.asr = ASR()
        self.tts = TTS()
        self.dm = DM()

        self.output = sim_stdin

        # TODO: isso deve ir pra config, preferencialmente num JSON
        self.SESSION_ID = 'tcc-chatbot'

    def run(self):

        session_client = dialogflow.SessionsClient(credentials=GOOGLE_APPLICATION_CREDENTIALS)
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, self.SESSION_ID)

        wait_keyword = True

        while True:

            try:
                if SILENT_MODE:
                    text_to_be_analyzed = input("[Client] <-- ").lower()
                else:
                    if wait_keyword:
                        self.asr.waitKeyword()
                    text_to_be_analyzed = self.asr.listen()

                if not text_to_be_analyzed:
                    print("[Client] Nada reconhecido")
                    continue
                else:
                    text_input = dialogflow.types.TextInput(
                        text=text_to_be_analyzed, 
                        language_code=DIALOGFLOW_LANGUAGE_CODE)
                    query_input = dialogflow.types.QueryInput(text=text_input)

                    try:
                        result = session_client.detect_intent(session=session, query_input=query_input)
                        response = self.dm.treatResult(result)
                        #response = {
                        #    "actions": [1,1,1,1,1,1,1,1,1],
                        #    "answer": None,
                        #    "end_conversation": True
                        #    }

                        # Acionamento
                        if SIMULATION:
                            #a = str(response['actions']) + '\n'
                            a = input("Digite:")
                            self.output.write(bytes(a, "ascii"))
                            self.output.flush()
                            self.output.seek(0)
                        else:
                            # Implementação real de acionamento
                            print("[Client] Acionamento:", response['actions'])

                        # Resposta falada
                        if response['answer'] and not SILENT_MODE:
                            self.tts.speak(response['answer'])

                        wait_keyword = response['end_conversation']

                    except Exception as e:
                        print("[Client] Erro ao tentar detectar a inteção:")
                        print("        ", e)

            except KeyboardInterrupt:
                print ("\n[Client] Parando cliente")
                break

def _send_data_to(proc, inp):
    proc.communicate(inp)
