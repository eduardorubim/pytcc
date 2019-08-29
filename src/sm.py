from owlready2 import *

class SemanticMemory:

    def __init__(self):
        self.onto = get_ontology("file://pytcc/smarthome/smarthome.owl").load(reload = True)
        onto_path.append("pytcc/smarthome/")

    """
    Retorna o numero de dispositivos total da casa
    """
    def getNumberOfDevices(self):
        # [0] corresponde a smarthome.SmartDevice
        return len(self.onto.search(is_a = self.onto.SmartDevice)) - 1

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
    sm.turnOn(sm.getIndoorPlaces()[3].hasSmartDevice[0])
    for place in sm.getIndoorPlaces():
        print (sm.getName(place))
        smart_devices = sm.getSmartDevices(place)
        for device in smart_devices:
            print("  " + str(sm.getDeviceIsOn(device)))
