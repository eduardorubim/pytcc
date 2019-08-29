# pytcc

## Dependências
[Crie e ative um ambiente virtual](https://docs.python.org/3/tutorial/venv.html) do Python. Depois instale a(s) dependência(s):

```sh
$ pip install -r requirements.txt
```

## Utilização

Ainda no ambiente virtual, execute `pytcc` com Python:

```sh
$ python pytcc
```

## Módulo TTS em MAC OS X

Note que, para sistemas MAC OS X, o módulo [playsound](https://pypi.org/project/playsound/) depende do módulo da AppKit.NSSound contido na biblioteca PyObjC (já incluido em `requirements.txt`). 

## Credenciais do Dialogflow

Deve-se gerar as credenciais do agente Dialogflow periodicamente e colocá-las em no diretório `/pytcc/credentials/`, alterando o nome no inicializador de `Client` apropriadamente.

## Simulador

O simulador se encontra em `simulation.py`. É possível observar mudanças na ontologia em tempo real. Execute-o com Python:

```sh
$ python pytcc/simulation.py
```