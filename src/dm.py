from owlready2 import *
import dialogflow_v2 as dialogflow
import json

from src.globals import *

"""
Classe do gerenciador de diálogo
"""
class DialogManager:

    def __init__(self):
        # Carrega as informacoes da memoria semantica (+ episodica)
        self.onto = get_ontology("file://configs/smarthome.owl").load(reload = True)
        onto_path.append("configs/")

        with open (ROUTINES_JSON_PATH, 'r+') as jfile:
            try:
                self.data = json.load(jfile)
                self.id = self.data['size'] - 1
            except Exception as e:
                print("* Overwriting routines file:", e)
                print("  Please, clean the Dialogflow project.")
                self.id = 0
                self.data = {"size": 1, "routines": []}
                self.data['routines'].append({
                    # vide DialogManager.treatResult()
                    "actions": [],
                    "parameters": []
                })
                json.dump(self.data, jfile)


    #################### FUNCOES "GET" BASICAS PARA AS CLASSES ####################

    """
    Retorna uma lista com os lugares (Place)
    """
    def getPlaces(self):
        # [0] corresponde a smarthome.Place
        # [1] corresponde a smarthome.IndoorPlace
        # [2] corresponde a smarthome.OutdoorPlace
        return self.onto.search(is_a = self.onto.Place)[3:]

    """
    Retorna uma lista com os lugares internos (IndoorPlace)
    """
    def getIndoorPlaces(self):
        # [0] corresponde a smarthome.Place
        return self.onto.search(is_a = self.onto.IndoorPlace)[1:]

    """
    Retorna o numero de dispositivos total da casa
    """
    def getOutdoorPlaces(self):
        # [0] corresponde a smarthome.Place
        return self.onto.search(is_a = self.onto.OutdoorPlace)[1:]

    """
    Retorna uma lista com os dispositivos (SmartDevice)
    """
    def getSmartDevices(self):
        # [0] corresponde a smarthome.SmartDevice
        return self.onto.search(is_a = self.onto.SmartDevice)[1:]

    """
    Retorna uma lista com o nomes (Names)
    * Names é uma classe contendo nomes (String)
    """
    def getNames(self):
        # [0] corresponde a smarthome.Names
        return self.onto.search(is_a = self.onto.Names)[1:]


    #################### FUNCOES "GET" PARA AS LOCAIS (PLACE) ####################

    """
    Retorna a lista de dispositivos de um local (Place)
    """
    def getPlaceSmartDevices(self, place):
        return place.hasSmartDevice

    """
    Retorna uma lista com os nomes (String) de um local (Place)
    """
    def getPlaceNames(self, place):
        return place.hasPlaceNames[0].hasNameValue

    #################### FUNCOES "GET" PARA OS DISPOSITIVOS (SMARTDEVICE) ####################

    """
    Retorna o numero de dispositivos total da casa
    """
    def getNumberOfDevices(self):
        return len(getSmartDevices)

    """
    Retorna uma lista com os nomes (String) de um dispositivo (SmartDevice)
    """
    def getSmartDeviceNames(self, smart_device):
        return smart_device.hasSmartDeviceNames[0].hasNameValue

    """
    Retorna o estado do dispositivo (SmartDevice)
    """
    def getDeviceIsOn(self, smart_device):
        return smart_device.isOn


    #################### FUNCOES "GET" PARA NOMES (STRING) E ETC ####################

    """
    Retorna um lugar (Place) baseado em um nome (String) (case independent)
    * Se não houver um nome correspondente, retorna None
    """
    def getPlaceFromName(self, name):
        name = name.lower()
        for place in self.getPlaces():
            for a_name in self.getPlaceNames(place):
                if a_name.lower() == name:
                    return place
        return None

    """
    Retorna um dispositivoo (SmartDevice) baseado em um nome (String) (case independent)
    e de um local (Place)
    * Se não houver um nome correspondente, retorna None
    """
    def getSmartDevicesFromNamePlace(self, name, place):
        name = name.lower()
        for device in self.getPlaceSmartDevices(place):
            for a_name in self.getSmartDeviceNames(device):
                if a_name.lower() == name:
                    return device
        return None

    #################### FUNCOES PARA LIGAR DISPOSITIVOS (DUMMY) ####################
    
    """
    Liga um dispositivo (SmartDevice)
    """
    def turnOn(self, smart_device):
        smart_device.isOn = True
        self.onto.save()

    """
    Liga um dispositivo (SmartDevice) utilizando os nomes (String) do dispositivo
    e do local
    """
    def turnOnFromSmartDeviceNamePlaceName(self, sm_name, p_name):
        place = self.getPlaceFromName(p_name)
        if place:
            smart_device = self.getSmartDevicesFromNamePlace(sm_name, place)
            if smart_device:
                self.turnOn(smart_device)
                return
        print ("[DialogManager] Local ou dispositivo nao encontrados")
        
    #################### FUNCOES PARA DESLIGAR DISPOSITIVOS (DUMMY) ####################

    """
    Desliga um dispositivo (SmartDevice)
    """
    def turnOff(self, smart_device):
        smart_device.isOn = False
        self.onto.save()

    """
    Desliga um dispositivo (SmartDevice) utilizando os nomes (String) do dispositivo
    e do local
    """
    def turnOffFromSmartDeviceNamePlaceName(self, sm_name, p_name):
        place = self.getPlaceFromName(p_name)
        if place:
            smart_device = self.getSmartDevicesFromNamePlace(sm_name, place)
            if smart_device:
                self.turnOff(smart_device)
                return
        print ("[DialogManager] Local ou dispositivo nao encontrados")

    #################### FUNCAO DUMMY DA API DE ACIONAMENTO ####################

    def do (self, action, parameters):
        if action.endswith(".on"):
            for sm_name in parameters['devices']:
                for p_name in parameters['places']:
                    self.turnOnFromSmartDeviceNamePlaceName(sm_name, p_name)
        elif action.endswith(".off"):
            for sm_name in parameters['devices']:
                for p_name in parameters['places']:
                    self.turnOffFromSmartDeviceNamePlaceName(sm_name, p_name)
        else:
            pass # outra acao 


    #################### FUNCAO PARA TRATAR O RESULTADO ####################

    """
    Decide a acao baseado no retorno do Dialogflow
    """
    def treatResult (self, result):

        # variável de retorno
        ret = {
            "actions": [],              # array de ações a serem executadas
            "parameters": [             # array com os parâmetros correspondentes a cada ação
                #{            
                    #"devices": [],     # array dos dispositivos da respectiva ação
                    #"places": []       # array dos lugares da respectiva ação
                #}
            ],
            "answer": None,             # resposta a ser falada (passada ao tts)
            "end_conversation": True    # flag para pedir a keyword de novo no próximo comando
        }

        print("[DialogManager] Query text:", result.query_result.query_text)
        print("[DialogManager] Detected intent:", result.query_result.intent.display_name)
        print("[DialogManager] Detected intent confidence:", result.query_result.intent_detection_confidence)
        print("[DialogManager] Detected parameters:")

        main_action = result.query_result.action

        # Ativar/desativar um 'device' em um 'place'
        if main_action.startswith("device."):
            ret['actions'].append(main_action)
            ret['parameters'].append({
                "devices": self._list2array(result.query_result.parameters.fields['device'].list_value),
                "places": self._list2array(result.query_result.parameters.fields['place'].list_value)
            })
            print("                device:", ret['parameters'][0]['devices'])
            print("                place :", ret['parameters'][0]['places'])

        # Criar uma rotina
        elif main_action.startswith("routine."):

            if main_action.endswith(".create"):
                print ("[DialogManager] Criando rotina id:", self.id)
                with open (ROUTINES_JSON_PATH, 'w') as jfile:
                    try: # tenta limpar se houver alguma coisa
                        self.data['routines'][self.id]['actions'] = []
                        self.data['routines'][self.id]['parameters'] = []
                    except: # não existe a estrutura nesse id
                        self.data['routines'].append({
                            "actions": [],
                            "parameters": []
                        })
                    json.dump(self.data, jfile)

            elif main_action.endswith("on.command"):
                with open (ROUTINES_JSON_PATH, 'w') as jfile:
                    self.data['routines'][self.id]['actions'].append("devices.on")
                    self.data['routines'][self.id]['parameters'].append({
                        "devices": self._list2array(result.query_result.parameters.fields['device'].list_value),
                        "places": self._list2array(result.query_result.parameters.fields['place'].list_value)
                    })
                    json.dump(self.data, jfile)

            elif main_action.endswith("off.command"):
                with open (ROUTINES_JSON_PATH, 'w') as jfile:
                    self.data['routines'][self.id]['actions'].append("devices.off")
                    self.data['routines'][self.id]['parameters'].append({
                        "devices": self._list2array(result.query_result.parameters.fields['device'].list_value),
                        "places": self._list2array(result.query_result.parameters.fields['place'].list_value)
                    })
                    json.dump(self.data, jfile)

            elif main_action.endswith("finish"):
                pass

            elif main_action.endswith("finish.command"):
                command = result.query_result.parameters.fields['phrase'].string_value
                display_name = "smarthome.user.command." + str(self.id)
                training_phrases_parts = [command]
                action = display_name + ":" + command.replace(' ', '-')
                print("[DialogManager] Tentando finalizar criação da rotina:")
                print("                Nome da rotina:", display_name)
                print("                Frase de ativação:", command)
                print("                Código da ação:", action)
                try:
                    self.createIntent(DIALOGFLOW_PROJECT_ID, display_name, training_phrases_parts, action)
                    self.id += 1
                    with open (ROUTINES_JSON_PATH, 'w') as jfile:
                        self.data['size'] += 1
                        json.dump(self.data, jfile)
                except Exception as e:
                    ret['answer'] = "Não foi possível criar a rotina"
                    print("[DialogManager] Não foi possível criar a rotina:")
                    print("               ", e)
            
            elif main_action.endswith(".delete"):
                pass

            elif main_action.endswith(".delete.command"):
                command = result.query_result.parameters.fields['phrase'].string_value
                try:
                    self.deleteCommand(command)
                    # Mantém o `routines.json` intacto, deleta apenas no Dialogflow
                    #self.id -= 1
                    #with open (ROUTINES_JSON_PATH, 'w') as jfile:
                    #    self.data['size'] = self.data['size'] - 1 if self.id > 0 else 1
                    #    json.dump(self.data, jfile)
                except Exception as e:
                    ret['answer'] = "Não foi possível deletar essa rotina"
                    print("[DialogManager] Não foi possível deletar a rotina:")
                    print("               ", e)
        
        # Rotinas criadas
        elif main_action.startswith("smarthome.user.command."):
            # procura o id da rotina na lista de rotinas (o ultimo id liberado é desconsiderado)
            for id_routine in range(self.data['size'] - 1):
                if (main_action.split('.')[3].startswith(str(id_routine))):
                    ret['actions'] = self.data['routines'][id_routine]['actions']
                    ret['parameters'] = self.data['routines'][id_routine]['parameters']
                    break
        
        # Fallback
        elif main_action.endswith(".cancel"):
            pass

        #else:
        #    print(result)

        # Texto para resposta falada (o texto do DialogManager tem prioridade)
        if not ret['answer']:
            ret['answer'] = result.query_result.fulfillment_text
        print("[DialogManager] Fulfillment text:", ret['answer'])

        # Finalizar conversa?
        ret['end_conversation'] = result.query_result.diagnostic_info.fields['end_conversation'].bool_value
        print("[DialogManager] End conversation:", ret['end_conversation'])

        # Contexto
        print("[DialogManager] Context:")
        for context in result.query_result.output_contexts:
            print("               ", context.name)

        return ret

    """
    Transforma list_value em um vetor Python
    """
    def _list2array(self, list_value):
        array = []
        for value in list_value:
            array.append(value)
        return array

    #################### FUNCOES PARA API DO DIALOGFLOW ####################

    """
    Cria uma intent (adaptado de https://cloud.google.com/dialogflow/docs/manage-intents)
    """
    def createIntent(self, project_id, display_name, training_phrases_parts, action):
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
            messages=[],
            end_interaction=True)

        response = intents_client.create_intent(parent, intent, language_code='pt-BR')

        print('Intent created: {}'.format(response))

    """
    Deleta uma intent (adaptado de https://cloud.google.com/dialogflow/docs/manage-intents)
    """
    def delete_intent(self, project_id, intent_id):
        intents_client = dialogflow.IntentsClient()

        intent_path = intents_client.intent_path(project_id, intent_id)

        intents_client.delete_intent(intent_path)

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

        self.delete_intent(DIALOGFLOW_PROJECT_ID, path)


    """
    Lista as intents (para DEBUG) (adaptado de https://cloud.google.com/dialogflow/docs/manage-intents)
    """
    def list_intents(self, project_id):
        intents_client = dialogflow.IntentsClient()

        parent = intents_client.project_agent_path(project_id)

        intents = intents_client.list_intents(parent)

        for intent in intents:
            print (intents_client.get_intent(intent.name, language_code='pt-BR'))
            """
            print('=' * 20)
            print('Intent name: {}'.format(intent.name))
            print('Intent display_name: {}'.format(intent.display_name))
            print('Action: {}\n'.format(intent.action))
            print('Root followup intent: {}'.format(
                intent.root_followup_intent_name))
            print('Parent followup intent: {}\n'.format(
                intent.parent_followup_intent_name))

            print('Input contexts:')
            for input_context_name in intent.input_context_names:
                print('\tName: {}'.format(input_context_name))

            print('Output contexts:')
            for output_context in intent.output_contexts:
                print('\tName: {}'.format(output_context.name))

            print('Training Phrases:')
            for phrase in intent.training_phrases:
                print('\tPhrase: {}'.format(phrase))
                """


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
    sm.list_intents(DIALOGFLOW_PROJECT_ID)