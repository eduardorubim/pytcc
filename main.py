import dialogflow
from google.api_core.exceptions import InvalidArgument

from tts import TTS
from asr import ASR

DIALOGFLOW_PROJECT_ID = 'newagent-7d078'
DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
GOOGLE_APPLICATION_CREDENTIALS = 'newagent-7d078-65fdc9af8063.json'
SESSION_ID = 'tcc-chatbot'

text_to_be_analyzed = ASR.listen()

session_client = dialogflow.SessionsClient()
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