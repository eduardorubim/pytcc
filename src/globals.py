from google.oauth2 import service_account
import os, sys

DIALOGFLOW_CREDENTIALS_PATH = "credentials/smart-home.json"
DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
ROUTINES_JSON_PATH = "configs/routines.json"

GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file(DIALOGFLOW_CREDENTIALS_PATH)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = DIALOGFLOW_CREDENTIALS_PATH

if len(sys.argv) > 1 and sys.argv[1] == "SILENT":
        SILENT_MODE = True
        print("* SILENT_MODE enabled: type your phrases at will.")
else:
    SILENT_MODE = False