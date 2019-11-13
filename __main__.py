from subprocess import Popen
from src.globals import *

# config

sim = None

try:
    if SIMULATION:
        sim = Popen(["python", "_simulation.py"])

    from src.client import Client
    client = Client()
    client.run()

except Exception as e:
    print("[main] Erro:", e)

finally:
    if not sim == None:
        print("[main] Parando a simulação")
        sim.terminate()
