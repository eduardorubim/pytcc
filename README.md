# pytcc

## Dependências
[Crie e ative um ambiente virtual](https://docs.python.org/3/tutorial/venv.html) do Python. Depois instale a(s) dependência(s):

```sh
$ pip install -r requirements.txt
```

## Utilização

Ainda no ambiente virtual, execute `pytcc` com Python:

```sh
$ python .
```

## Módulo TTS em MAC OS X

Note que, para sistemas MAC OS X, o módulo [playsound](https://pypi.org/project/playsound/) depende do módulo da AppKit.NSSound contido na biblioteca PyObjC (já incluido em `requirements.txt`). 

## Credenciais do Dialogflow

Deve-se gerar as credenciais do agente Dialogflow periodicamente e colocá-las no diretório `/pytcc/credentials/`, alterando o nome em `pytcc/src/globals.py` apropriadamente.

## Simulador

O simulador se encontra em `_simulation.py`. É possível observar mudanças no esquema simplificado da residência em tempo real. Para chamar a aplicação com o simulador:

```sh
$ python . SIMULATE
```

## Exportando entidades para o Dialogflow

É possível criar um `.csv` para realizar o Upload de entidades no Dialogflow. Rode o `_export.py` após criar os indivíduos em `pytcc/smarthome/smarthome.owl`:

```sh
$ python _export.py
```

Em seguida, vá até a aba Entities do seu Dialogflow Agent, clique na opção Upload Entity oculta ao lado de Create Entity e selecione o arquivo `.csv` gerado em `pytcc/smarthome/`.
