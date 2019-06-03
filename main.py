import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account

from tts import TTS
from asr import ASR

DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('/credentials/smart-home-1-6c30f-b1024858ceb7.json')
SESSION_ID = 'tcc-chatbot'

text_to_be_analyzed = ASR.listen()

session_client = dialogflow.SessionsClient(credentials=GOOGLE_APPLICATION_CREDENTIALS)
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
try:
    response = session_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raise

print("Query text:", response.query_result.query_text)
print("Detected intent:", response.query_result.intent.display_name)
print("Detected intent confidence:", response.query_result.intent_detection_confidence)
print("Fulfillment text:", response.query_result.fulfillment_text)

TTS.speak(response.query_result.fulfillment_text)
#TTS.speak(ASR.listen())