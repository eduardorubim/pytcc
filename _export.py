from src.dm import DialogManager
import csv

class ExportCSV:

    def __init__(self):
        # Carregando a memoria
        self.data = DialogManager()

    def generatePlaceCSV(self):
        with open ('pytcc/smarthome/place.csv', mode='w') as memory:
            csv_writer = csv.writer(memory, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for place in self.data.getPlaces():
                names = self.data.getPlaceNames(place)
                names.insert(0, names[0])
                print(names)
                csv_writer.writerow(names)

if __name__ == "__main__":
    ex = ExportCSV()
    ex.generatePlaceCSV()