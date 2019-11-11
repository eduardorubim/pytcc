from src.globals import *

# config

try:
    from src.client import Client
    client = Client()
    client.run()

except Exception as e:
    print("[main] Erro:", e)
