from subprocess import PIPE, Popen
from src.globals import *
import tempfile

# config

simul = None
tf = None
try:
    if SIMULATION:
        tf = tempfile.TemporaryFile()
        simul = Popen(["python", "-u", "_simulation.py"], stdin=tf, stdout=None, text=True)

    from src.client import Client
    client = Client(tf)
    client.run()

finally:
    if not simul == None:
        simul.terminate()
        print ("[__main__] Parando simulação")
    if not tf == None:
        tf.close()

