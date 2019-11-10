from owlready2 import *

"""
Classe que carrega a memória semântica
"""
class SemanticMemory:

    def __init__(self):
        # Carrega as informacoes da memoria semantica (+ episodica)
        self.onto = get_ontology("file://configs/smarthome.owl").load(reload = True)
        onto_path.append("configs/")
        # Monta o vetor de dispositivos com id(portas) em ordem crescente
        self.devices_id = []
        for device in self.getSmartDevices():
            self.devices_id.append(self.getSmartDeviceId(device))
        self._sort(self.devices_id)
    
    # Selection sort
    def _sort(self, array):
        for i in range(len(array)):
            lowest_i = i
            for j in range(i+1,len(array)):
                if array[j] < array[lowest_i]:
                    array[lowest_i], array[j] = array[j], array[lowest_i]
        return array

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
    Retorna uma lista com os nomes (Names)
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
        return len(self.getSmartDevices())

    """
    Retorna uma lista com os nomes (String) de um dispositivo (SmartDevice)
    """
    def getSmartDeviceNames(self, smart_device):
        return smart_device.hasSmartDeviceNames[0].hasNameValue

    """
    Retorna o id de um dispositivo (SmartDevice)
    """
    def getSmartDeviceId(self, smart_device):
        return smart_device.hasIdValue

    """
    Retorna o índice do dispositivo (SmartDevice) no devices_id (array)
    """
    def getSmartDeviceIndex(self, smart_device):
        return self.devices_id.index(self.getSmartDeviceId(smart_device))

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
    Retorna um dispositivo (SmartDevice) baseado em um nome (String) (case independent)
    e um local (Place)
    * Se não houver um nome correspondente, retorna None
    """
    def getSmartDeviceFromNamePlace(self, name, place):
        name = name.lower()
        for device in self.getPlaceSmartDevices(place):
            for a_name in self.getSmartDeviceNames(device):
                if a_name.lower() == name:
                    return device
        return None

    """
    Retorna um dispositivo (SmartDevice) baseado em um idNum (int)
    * Se não houver um nome correspondente, retorna None
    """
    def getSmartDeviceFromId(self, idNum):
        for device in self.getSmartDevices():
            if self.getSmartDeviceId(device) == idNum:
                return device
        return None

    """
    Retorna um dispositivo (SmartDevice) em nomes: 
    dispositivo (String), local (String) 
    * Se não houver um nome correspondente, retorna None
    """
    def getSmartDeviceFromNames(self, device_s, place_s):
        place = self.getPlaceFromName(place_s)
        if place:
            return self.getSmartDeviceFromNamePlace(device_s, place)
        else:
            return None

if __name__ == '__main__':
    sm = SemanticMemory()
    a = [9,8,0,6,40,4,3,2,1]
    print (sm._sort(a))
