import subprocess

# config

try:
    simulation = subprocess.Popen(["python", "_simulation.py"])

    from src.client import Client
    client = Client()
    client.run()

finally:
    simulation.terminate()
