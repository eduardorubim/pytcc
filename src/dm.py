from owlready2 import *
import dialogflow_v2 as dialogflow
import json

from src.globals import *
from src.sm import SemanticMemory

"""
Classe do gerenciador de diálogo
"""
class DialogManager:

    def __init__(self):
        # Carrega as informacoes da memoria semantica (+ episodica)
        self.sm = SemanticMemory()
        self.num_of_dev = self.sm.getNumberOfDevices()

        with open (ROUTINES_JSON_PATH, 'r+') as jfile:
            try:
                self.data = json.load(jfile)
                self.id = self.data['size'] - 1
            except Exception as e:
                print("* Overwriting routines file:", e)
                print("  Please, clean the Dialogflow project.")
                self.id = 0
                self.data = {"size": 1, "routines": []}
                self.data['routines'].append([0 for _ in range(self.num_of_dev)])
                json.dump(self.data, jfile)

    #################### FUNCOES PARA TRATAR O RESULTADO ####################

    """
    Decide a acao baseado no retorno do Dialogflow
    """
    def treatResult (self, result):

        # variável de retorno
        ret = {
            "actions": [0 for _ in range(self.num_of_dev)],   # array de ações a serem executadas
            "answer": None,             # resposta a ser falada (passada ao tts)
            "end_conversation": None    # flag para pedir a keyword de novo no próximo comando
        }

        cmd = {
            "on" : 1,
            "off": 0
        }

        print("[DialogManager] Query text:", result.query_result.query_text)
        print("[DialogManager] Detected intent:", result.query_result.intent.display_name)
        print("[DialogManager] Detected intent confidence:", result.query_result.intent_detection_confidence)
        print("[DialogManager] Detected parameters:")

        main_action = result.query_result.action.split('.')
        last = len(main_action) - 1

        # Ativar/desativar um 'device' em um 'place'
        if main_action[0] == "device":
            places, devices = self._getParam(result, ["place", "device"])
            ret['answer'] = self._checkPlacesSmartDevices(places, devices)
            for place_s in places:
                for device_s in devices:
                    device = self.sm.getSmartDeviceFromNames(device_s, place_s)
                    self.em[self.sm.getSmartDeviceIndex(device)] = cmd[main_action[last]] # on/off
            ret['actions'] = self.em
            print("                device:", devices)
            print("                place :", places)

        # Rotinas
        elif main_action[0] == "routine":

            if main_action[1] == "create":

                if main_action[last] == "create":
                    print ("[DialogManager] Criando rotina id:", self.id)
                    with open (ROUTINES_JSON_PATH, 'w') as jfile:
                        try: # tenta limpar se houver alguma coisa
                            self.data['routines'][self.id] = [0 for _ in range(self.num_of_dev)]
                        except: # não existe a estrutura nesse id
                            self.data['routines'].append([0 for _ in range(self.num_of_dev)])
                        json.dump(self.data, jfile)

                elif main_action[last] == "on" or main_action[last] == "off":
                    places, devices = self._getParam(result, ["place", "device"])
                    ret['answer'] = self._checkPlacesSmartDevices(places, devices)
                    if not ret['answer']:
                        with open (ROUTINES_JSON_PATH, 'w') as jfile:
                            for place_s in places:
                                for device_s in devices:
                                    device = self.sm.getSmartDeviceFromNames(device_s, place_s)
                                    self.data['routines'][self.id][self.sm.getSmartDeviceIndex(device)] = cmd[main_action[last]] #on/off
                            json.dump(self.data, jfile)

                elif main_action[2] == "finish":

                    if main_action[last] == "finish":
                        # Mudança de contexto para create.finish.command
                        pass

                    elif main_action[last] == "command":
                        command = result.query_result.parameters.fields['phrase'].string_value
                        display_name = "user.command." + str(self.id)
                        training_phrases_parts = [command]
                        action = display_name + ":" + command.replace(' ', '-')
                        print("[DialogManager] Tentando finalizar criação da rotina:")
                        print("                Nome da rotina:", display_name)
                        print("                Frase de ativação:", command)
                        print("                Código da ação:", action)
                        try:
                            self.createCommand(DIALOGFLOW_PROJECT_ID, display_name, training_phrases_parts, action)
                            self.id += 1
                            with open (ROUTINES_JSON_PATH, 'w') as jfile:
                                self.data['size'] += 1
                                json.dump(self.data, jfile)
                        except Exception as e:
                            ret['answer'] = "Não foi possível criar a rotina"
                            print("[DialogManager] Não foi possível criar a rotina:")
                            print("               ", e)

            elif main_action[1] == "delete":

                if main_action[last] == "delete":
                    # Mudança de contexto para delete.command
                    pass

                if main_action[last] == "command":
                    command = result.query_result.parameters.fields['phrase'].string_value
                    try:
                        self.deleteCommand(command)
                        # Mantém o `routines.json` intacto, deleta apenas no Dialogflow
                    except Exception as e:
                        ret['answer'] = "Não foi possível deletar essa rotina"
                        print("[DialogManager] Não foi possível deletar a rotina:")
                        print("               ", e)
        
        # Execução das Rotinas criadas
        elif main_action[0] == "user":
            # procura o id da rotina na lista de rotinas (o ultimo id liberado é desconsiderado)
            for routine_id in range(self.data['size'] - 1):
                if (main_action[last].startswith(str(routine_id))):
                    for i, act in enumerate(self.data['routines'][routine_id]):
                        if act != -1:
                            self.em[i] = act
                    ret['actions'] = self.em
                    ret['end_conversation'] = True
                    break
        
        # Fallback
        elif main_action[0] == "cancel":
            pass

        #else:
        #    print(result)

        # Texto para resposta falada (o texto do DialogManager tem prioridade)
        if not ret['answer']:
            ret['answer'] = result.query_result.fulfillment_text
        print("[DialogManager] Fulfillment text:", ret['answer'])

        # Finalizar conversa? (o DialogManager tem prioridade)
        if ret['end_conversation'] == None:
            ret['end_conversation'] = result.query_result.diagnostic_info.fields['end_conversation'].bool_value
        print("[DialogManager] End conversation:", ret['end_conversation'])

        # Contexto
        print("[DialogManager] Context:")
        for context in result.query_result.output_contexts:
            print("               ", context.name)

        return ret

    """
    Transforma list_value em um vetor Python (array)
    """
    def _list2array(self, list_value):
        array = []
        for value in list_value:
            array.append(value)
        return array

    """
    Retorna as listas (array) correspondentes a cada field (String)
    advindos do resultado do Dialogflow (result)
    """
    def _getParam(self, result, field_names):
        ret = []
        for param in field_names:
            ret.append(self._list2array(result.query_result.parameters.fields[param].list_value))
        return ret

    """
    Verifica se os locais (String array) ou os dispositivos (String array) existem.
    Retorna a frase (String) correspondente para ret['answer'], None se encontrados
    """
    def _checkPlacesSmartDevices(self, places, devices):
        answer = ""
        for place in places:
            place_obj = self.sm.getPlaceFromName(place)
            if place_obj:
                for device in devices:
                    if not self.sm.getSmartDeviceFromNamePlace(device, place_obj):
                        answer = "Dispositivo não encontrado"
                        devices = []
                        break
            else:
                answer = "Local não encontrado"
                places = []
                break
        return answer

    #################### FUNCOES PARA API DO DIALOGFLOW ####################

    """
    Cria uma intent (comando) (adaptado de https://cloud.google.com/dialogflow/docs/manage-intents)
    """
    def createCommand(self, project_id, display_name, training_phrases_parts, action):
        intents_client = dialogflow.IntentsClient()

        parent = intents_client.project_agent_path(project_id)
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_phrases_part)
            # Here we create a new training phrase for each provided part.
            training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        intent = dialogflow.types.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            action=action,
            messages=[])

        response = intents_client.create_intent(parent, intent, language_code='pt-BR')

        print('Intent created: {}'.format(response))

    """
    Deleta uma rotina (intent) baseada no comando dado (criado por um usuario)
    """
    def deleteCommand(self, command):
        intents_client = dialogflow.IntentsClient()
        path = ""

        parent = intents_client.project_agent_path(DIALOGFLOW_PROJECT_ID)
        intents = intents_client.list_intents(parent)
        
        # procurando a intent cuja acao confere com a do comando dito
        for intent in intents:
            if intent.action.endswith(":" + command.replace(' ', '-')):
                path = '/'.join(intent.name.split('/')[4:]) # formatando para projects/*/agent/intents/*
                break

        self._delete_intent(DIALOGFLOW_PROJECT_ID, path)

    """
    Deleta uma intent (adaptado de https://cloud.google.com/dialogflow/docs/manage-intents)
    """
    def _delete_intent(self, project_id, intent_id):
        intents_client = dialogflow.IntentsClient()

        intent_path = intents_client.intent_path(project_id, intent_id)

        intents_client.delete_intent(intent_path)


    """
    Lista as intents (para DEBUG) (adaptado de https://cloud.google.com/dialogflow/docs/manage-intents)
    """
    def _list_intents(self, project_id):
        intents_client = dialogflow.IntentsClient()

        parent = intents_client.project_agent_path(project_id)

        intents = intents_client.list_intents(parent)

        for intent in intents:
            print (intents_client.get_intent(intent.name, language_code='pt-BR'))
            # print('=' * 20)
            # print('Intent name: {}'.format(intent.name))
            # print('Intent display_name: {}'.format(intent.display_name))
            # print('Action: {}\n'.format(intent.action))
            # print('Root followup intent: {}'.format(
            #     intent.root_followup_intent_name))
            # print('Parent followup intent: {}\n'.format(
            #     intent.parent_followup_intent_name))

            # print('Input contexts:')
            # for input_context_name in intent.input_context_names:
            #     print('\tName: {}'.format(input_context_name))

            # print('Output contexts:')
            # for output_context in intent.output_contexts:
            #     print('\tName: {}'.format(output_context.name))

            # print('Training Phrases:')
            # for phrase in intent.training_phrases:
            #     print('\tPhrase: {}'.format(phrase))


if __name__ == "__main__":
    sm = DialogManager()
    #sm.turnOn(sm.getIndoorPlaces()[3].hasSmartDevice[0])
    #for place in sm.getIndoorPlaces():
    #    print (sm.getPlaceNames(place))
    #    smart_devices = sm.getPlaceSmartDevices(place)
    #    for device in smart_devices:
    #        print("  " + str(sm.getDeviceIsOn(device)))
    #places = sm.getPlaceFromName("Quarto do joão")
    #print(sm.getPlaceNames(places[0]))
    #sm.turnOffFromSmartDeviceNamePlaceName("Luz", "Sala")
    sm._list_intents(DIALOGFLOW_PROJECT_ID)