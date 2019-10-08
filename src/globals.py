from google.oauth2 import service_account
import os
import subprocess

DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
ROUTINES_JSON_PATH = "configs/routines.json"

GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('credentials/smart-home.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials/smart-home.json"

SILENT_MODE = True