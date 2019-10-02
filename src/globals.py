from google.oauth2 import service_account

DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('pytcc/credentials/smart-home.json')
ROUTINES_JSON_PATH = "pytcc/configs/routines.json"
