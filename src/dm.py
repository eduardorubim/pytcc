from owlready2 import *

"""
Classe do gerenciador de diálogo
"""
class DialogManager:

    # Carrega as informacoes da memoria semantica (+ episodica)
    def __init__(self):
        self.onto = get_ontology("file://pytcc/smarthome/smarthome.owl").load(reload = True)
        onto_path.append("pytcc/smarthome/")

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
        print ("Local ou dispositivo nao encontrados")
        
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
        print ("Local ou dispositivo nao encontrados")


    #################### FUNCAO PARA TRATAR O RESULTADO ####################

    """
    Decide a acao baseado no retorno do Dialogflow
    ret = [intent, parameters, response message, end conversation]
    """
    def treatResult (self, result):

        intent_name = result.query_result.intent.display_name
        ret = [intent_name]

        print("[DialogManager]Query text:", result.query_result.query_text)
        print("[DialogManager]Detected intent:", intent_name)
        print("[DialogManager]Detected intent confidence:", result.query_result.intent_detection_confidence)
        print("[DialogManager]Detected parameters:")

        # Ativar/desativar um 'device' em um 'place'
        if intent_name.startswith("smarthome.device."):
            device_name = result.query_result.parameters.fields['device'].string_value
            place_name = result.query_result.parameters.fields['place'].string_value 
            print("               device:", device_name)
            print("               place :", place_name)
            ret.append([device_name, place_name])

        # Criar uma rotina
        elif intent_name.startswith("smarthome.routine."):
            ret.append([])
            # .create:
                # nada
            # .create-command.on:
                # device_name = String
                # place_names = [String]
                # ...armazenar... <<---------------------------------------------- json?
            # .create-command.off:
                # Análogo a .create-command.on
            # .create-finish:
                # nada
            # .create-finish.command:
                # command = result.query_result.parameters.fields['phrase'].string_value
                # createIntent(project_id
                #   diplay_name = "alguma coisa padronizada especial"
                #   training_phrases_parts = [command]
                #   message_texts = "")
            
            # .delete:
                # deleteIntent(project_id, intent_id = display_name)
        
        # Rotinas criadas
        # elif intent_name.startswith("a coisa padronizada especial"):
            # ret.append([])
            # for id in lista_de_rotinas:
                # if id == "resto da coisa padronizada especial":
                    # ret[1] = [id.device_name, """ id.place_names """  ]
                    # break
                

        # Nada
        else:
            print(result.query_result.parameters)
            ret.append([])

        # Texto para resposta falada
        fulf_text = result.query_result.fulfillment_text
        print("[DialogManager]Fulfillment text:", fulf_text)
        ret.append(fulf_text)

        # Finalizar conversa?
        ret.append(result.query_result.diagnostic_info.fields['end_conversation'].bool_value)

        #print(result)

        return ret

    #################### FUNCOES PARA API DO DIALOGFLOW ####################

    """
    Cria uma intent
    """
    def createIntent(project_id, display_name, training_phrases_parts, message_texts):
        import dialogflow_v2 as dialogflow
        intents_client = dialogflow.IntentsClient()

        parent = intents_client.project_agent_path(project_id)
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_phrases_part)
            # Here we create a new training phrase for each provided part.
            training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.types.Intent.Message.Text(text=message_texts)
        message = dialogflow.types.Intent.Message(text=text)

        intent = dialogflow.types.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message])

        response = intents_client.create_intent(parent, intent)

        print('Intent created: {}'.format(response))

    """
    Deleta uma intent
    """
    def delete_intent(project_id, intent_id):
        import dialogflow_v2 as dialogflow
        intents_client = dialogflow.IntentsClient()

        intent_path = intents_client.intent_path(project_id, intent_id)

        intents_client.delete_intent(intent_path)



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
    sm.turnOffFromSmartDeviceNamePlaceName("Luz", "Sala")