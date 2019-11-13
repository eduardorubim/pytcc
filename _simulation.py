import pygame
import socket
from multiprocessing import Process, Queue

from src.sm import SemanticMemory

HOST = '127.0.0.1'
PORT = 31415

class Driver:

    def __init__(self):
        # Carregando o mapa da casa
        self.home = SemanticMemory()
        self.in_places = self.home.getIndoorPlaces()
        self.out_places = self.home.getOutdoorPlaces()
        # Estado inicial
        self.state = [0 for _ in range(self.home.getNumberOfDevices())]
        # pygame
        pygame.init()
        pygame.font.init()
        # Fonte para textos
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 18)
        # Tamanhos arbitrários
        self.margin = 14
        self.screen_width  = 500
        self.screen_height = 500
        self.place_unit_size = 90
        # Posição do cursor para desenhar
        self.cursor = {"X": 0, "Y": 0}

    """ Retorna o cursor (tuple) """
    def _cursor(self):
        return (self.cursor['X'], self.cursor['Y'])

    """
    Desenha os cômodos da casa com seus respectivos dispositivos
    """
    def drawHome(self):
        # Janela principal
        screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        screen.fill((224, 224, 224))

        inex = {"INTERIOR": self.in_places, "EXTERIOR": self.out_places}
        for inex_str in inex:
            # Desenha header
            self.cursor['X'] += self.margin
            self.cursor['Y'] += self.margin
            text_s = self.font.render(inex_str, True, (0,0,0))
            screen.blit(text_s, self._cursor())
            # Desenha lugares
            self.cursor['Y'] += 2*self.margin
            for place in inex[inex_str]:
                try:
                    self.drawPlace(screen, place)
                    self.cursor['Y'] -= self.margin
                    self.cursor['X'] += self.margin
                except Exception as e:
                    print("[Driver] drawHome error:", e)
            # Próxima linha (para imprimir EXTERIOR)
            self.cursor['X'] = 0
            self.cursor['Y'] += (self.place_unit_size + 2*self.margin)
        # Reseta para próximo desenho
        self.cursor['X'] = 0
        self.cursor['Y'] = 0
        self.dev_id = 0
            
    """
    Desenha os dispositivos do local (Place) na janela (Surface)
    """
    def drawPlace(self, screen, place):
        devices = self.home.getPlaceSmartDevices(place)
        n_devs = len(devices)
        # Verifica se tem espaço
        if self.cursor['X'] > self.screen_width - n_devs*self.place_unit_size:
            self.cursor['X'] = self.margin
            self.cursor['Y'] += (self.place_unit_size + 2*self.margin)
        # Desenha o nome do local (primeiro nome)
        text_s = self.font.render(self.home.getPlaceNames(place)[0], True, (0,0,0))
        screen.blit(text_s, self._cursor())
        # Desenha os dispositivos
        self.cursor['Y'] += self.margin
        for device in devices:
            if self.state[self.home.getSmartDeviceIndex(device)] > 0:
                dev_state = "on"
            else:
                dev_state = "off"
            img_path = "grf/" + dev_state + "/" + self.home.getSmartDeviceNames(device)[0] + ".png"
            device_s = pygame.image.load(img_path).convert()
            screen.blit(device_s, self._cursor())
            # Próximo dispositivo
            self.cursor['X'] += self.place_unit_size

    """
    Socket listener
    """
    def f(self, q):
        while True: # precisa reabrir o socket toda vez
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    #print("[Driver] Conectado:", addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        else:
                            #print("[Driver] Recebido:", data)
                            q.put(data)
    """
    Roda a simulacao
    """
    def run(self):

        q = Queue()
        p = Process(target=self.f, args=(q,))
        p.start()

        refresh = False
        next_state = str(self.state)
        self.drawHome()
        pygame.display.flip()
        try:
            while True:
                #print("________")
                if refresh:
                    next_state = str(q.get().decode()).strip()
                    #print("[Driver] Acionamento:", next_state)
                    if next_state:
                        # Input do tipo "[-1,0,1]. -1: desliga, 0: mantém, 1: liga"
                        next_state = [int(x) for x in next_state[1:len(next_state)-1].split(',')]
                        for i in range(len(self.state)):
                            if next_state[i]:
                                self.state[i] = next_state[i]
                refresh = not refresh
                self.drawHome()
                pygame.display.flip()
                
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print("[Driver] run error:", e)
        finally:
            pygame.quit()

if __name__ == '__main__':
    driver = Driver()
    driver.run()
