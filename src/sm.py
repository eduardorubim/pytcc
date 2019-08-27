from owlready2 import *

class SemanticMemory:

    def __init__(self):
        self.onto = get_ontology("file://pytcc/smarthome/smarthome.owl").load()
        self.indoor_places = self.onto.search(is_a = self.onto.IndoorPlace)
        self.outdoor_places = self.onto.search(is_a = self.onto.OutdoorPlace)

if __name__ == "__main__":
    sm = SemanticMemory()
    smart_device = sm.indoor_places[1].hasSmartDevice
    print(sm.indoor_places[1].isNamed)
    print(smart_device[0].isOn)
