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
        # Funcao que ligaria o dispositivo fisico
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
        # Função que desligaria o dispostivo físico
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
    * `ret` é a variável de retorno, e depende muito de como a API de acionamentos seria configurada
    * a implementação a seguir é um dummy: ret = [intent, parameters, response message]
    """
    def treatResult (self, result):

        intent_name = result.query_result.intent.display_name
        ret = [intent_name]

        print("[DialogManager]Query text:", result.query_result.query_text)
        print("[DialogManager]Detected intent:", intent_name)
        print("[DialogManager]Detected intent confidence:", result.query_result.intent_detection_confidence)
        print("[DialogManager]Detected parameters:")

        # Ligar o 'device' em 'place'
        if intent_name == "smarthome.device.switch.on":
            device_name = result.query_result.parameters.fields['device'].string_value
            place_name = result.query_result.parameters.fields['place'].string_value 
            print("               device:", device_name)
            print("               place :", place_name)
            ret.append([device_name, place_name])
            self.turnOnFromSmartDeviceNamePlaceName(device_name, place_name)

        # Desligar o 'device' em 'place'
        elif intent_name == "smarthome.device.switch.off":
            device_name = result.query_result.parameters.fields['device'].string_value
            place_name = result.query_result.parameters.fields['place'].string_value
            print("               device:", device_name)
            print("               place :", place_name)
            ret.append([device_name, place_name])
            self.turnOffFromSmartDeviceNamePlaceName(device_name, place_name)

        # Default
        else:
            print(result.query_result.parameters)
            ret.append([])

        fulf_text = result.query_result.fulfillment_text
        print("[DialogManager]Fulfillment text:", fulf_text)
        ret.append(fulf_text)

        return ret


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