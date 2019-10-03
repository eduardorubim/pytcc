from google.oauth2 import service_account
import platform
import subprocess

DIALOGFLOW_PROJECT_ID = 'smart-home-1-6c30f'
DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('pytcc/credentials/smart-home.json')
ROUTINES_JSON_PATH = "pytcc/configs/routines.json"

os = platform.system()
try:
    if (os == 'Darwin' or os == 'Linux'):
            subprocess.call(['./pytcc/configs/bash.sh'])
    elif (os == 'Windows'):
        subprocess.Popen(['pytcc/configs/cmd.cmd'])
except Exception as e:
    print(e)
    print("Manually setting the environment variable GOOGLE_APPLICATION_CREDETIALS may be necessary")