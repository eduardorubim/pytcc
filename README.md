# pytcc

## Dependências
[gTTS](https://gtts.readthedocs.io/en/latest/#) e dependências.

[playsound](https://pypi.org/project/playsound/) e dependências.

[SpeechRecognition](https://pypi.org/project/SpeechRecognition/) e dependências.

## Módulo TTS em MAC OS X

O módulo playsound depende do módulo da AppKit.NSSound contido na biblioteca PyObjC. Não confundir com [AppKit](https://appkit.readthedocs.io/en/latest/index.html).

[Crie e ative um ambiente virtual](https://docs.python.org/3/tutorial/venv.html) do Python. Depois instale a(s) dependência(s). E.g.:

```sh
$ pip install -U pyobjc
```