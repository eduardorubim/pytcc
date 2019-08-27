from owlready2 import *

class SemanticMemory:

    def __init__(self):
        self.onto = get_ontology("file://pytcc/smarthome/smarthome.owl").load()
        self.indoor_places = self.onto.search(is_a = self.onto.IndoorPlace)
        self.outdoor_places = self.onto.search(is_a = self.onto.OutdoorPlace)
        onto_path.append("pytcc/smarthome/")

    """
    Retorna o nome (String) dado um local (Place)
    """
    def getName(self, place):
        return place.isNamed

    """
    Retorna a lista de dispositivos de um local (Place)
    """
    def getSmartDevices(self, place):
        return place.hasSmartDevice

    """
    Retorna o estado do dispositivo (SmartDevice)
    """
    def getDeviceIsOn(self, smart_device):
        return smart_device.isOn

    """
    Liga um dispositivo (SmartDevice)
    """
    def turnOn(self, smart_device):
        smart_device.isOn = True
        self.onto.save()

    """
    Desliga um dispositivo (SmartDevice)
    """
    def turnOff(self, smart_device):
        smart_device.isOn = False
        self.onto.save()    


if __name__ == "__main__":
    sm = SemanticMemory()
    for place in sm.indoor_places[1:]:
        print (sm.getName(place))
        smart_devices = sm.getSmartDevices(place)
        for device in smart_devices:
            print("  " + str(sm.getDeviceIsOn(device)))
            
    #sm.turnOn(sm.indoor_places[1].hasSmartDevice[0])
    #print(sm.indoor_places[1].hasSmartDevice[0].isOn)
