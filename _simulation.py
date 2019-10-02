import os
import pygame
import pygame.gfxdraw
from src.dm import DialogManager

class Simulation:

    def __init__(self):
        # Carregando a memoria
        self.smarthome = DialogManager()
        self.in_places = self.smarthome.getIndoorPlaces()
        self.out_places = self.smarthome.getOutdoorPlaces()
        self.n_in_places = len(self.in_places)
        self.n_out_places = len(self.out_places)
        # Arranjando os tamanhos
        self.unit_width = 90
        self.unit_height = 90
        self.space = 5
        self.head = 20
        # Divide os lugares em 5 colunas
        self.n_cols = 5
        self.n_in_rows = self.n_in_places // self.n_cols + (self.n_in_places % self.n_cols > 0)
        self.n_out_rows = self.n_out_places // self.n_cols + (self.n_out_places % self.n_cols > 0)
        self.screen_width = 4*self.space + self.n_cols * (self.unit_width + 2*self.space)
        self.screen_height = 4*self.space + (self.n_in_rows + self.n_out_rows) * (self.unit_height + 2*self.space) + 2*self.head
        # pygame
        pygame.init()
        pygame.font.init()
        # Fonte para textos
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 18)

    """
    Recarrega a memoria
    """
    def refresh(self):
        self.smarthome = DialogManager()
        self.in_places = self.smarthome.getIndoorPlaces()
        self.out_places = self.smarthome.getOutdoorPlaces()

    """
    Desenha o quadrado em uma superficie (Surface) dado o local (Place),
    com seus dispositivos (SmartDevice) e seus estados
    """
    def drawPlace(self, surface, place):
        # Desenhando o rótulo
        text_s = self.font.render(self.smarthome.getPlaceNames(place)[0], True, (0,0,0))
        surface.blit(text_s, (self.space, self.space))
        # Desenhando o local
        pygame.gfxdraw.rectangle(surface, 
                                (0, 0, self.unit_width, self.unit_height),
                                (0, 0, 0))
        # Dividindo o lugar para colocar os dispositivos
        devices = self.smarthome.getPlaceSmartDevices(place)
        n_devs = len(devices)
        n_cols = int(n_devs ** 0.5 + 0.5)
        n_rows = n_devs // n_cols + (n_devs % n_cols > 0)
        horz_space = self.unit_width // (n_cols+1)
        vert_space = self.unit_height // (n_rows+1)
        # Desenhando os dispositivos
        k = 0
        for i in range(n_rows):
            for j in range(n_cols):
                if k < n_devs:
                    device = devices[k]
                    k += 1
                    if self.smarthome.getDeviceIsOn(device):
                        light_color = (255, 255, 0)
                    else:
                        light_color = (0, 0, 0)
                    pygame.gfxdraw.filled_circle(surface,
                                                (i+1)*vert_space, (j+1)*horz_space, 6,
                                                light_color)
    
    """
    Desenha os comodos da smarthome com seus respectivos dispositivos
    """
    def drawSmartHome(self):
        # Janela principal
        screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        screen.fill((255, 255, 255))
        # Dividindo a janela para colocar os lugares
        horz_space = self.unit_width + self.space
        vert_space = self.unit_height + self.space
        # Desenhando os lugares internos
        text_s = self.font.render("INTERIOR", True, (0,0,0))
        screen.blit(text_s, (self.space, self.space))
        k = 0
        for i in range(self.n_in_rows):
            for j in range(self.n_cols):
                if k < self.n_in_places:
                    place_s = pygame.Surface((self.unit_width, self.unit_height), pygame.SRCALPHA)
                    self.drawPlace(place_s, self.in_places[k])
                    k += 1
                    screen.blit(place_s, (j*(self.space + horz_space) + 2*self.space, i*(self.space + vert_space) + self.head))
        # Desenhando os lugares externos
        text_s = self.font.render("EXTERIOR", True, (0,0,0))
        screen.blit(text_s, (self.space, self.space + self.n_in_rows*(self.space + vert_space) + self.head))
        k = 0
        for i in range(self.n_out_rows):
            for j in range(self.n_cols):
                if k < self.n_out_places:
                    place_s = pygame.Surface((self.unit_width, self.unit_height), pygame.SRCALPHA)
                    self.drawPlace(place_s, self.out_places[k])
                    k += 1
                    screen.blit(place_s, (j*(self.space + horz_space) + 2*self.space, (i+self.n_in_rows)*(self.space + vert_space) + 2*self.head))

    """
    Roda a simulacao
    """
    def run(self):

        last_mod_date = os.stat("pytcc/configs/smarthome.owl")[8]
        self.drawSmartHome()
        pygame.display.flip()
        try:
            while 1:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                        break
                new_date = os.stat("pytcc/configs/smarthome.owl")[8]
                if new_date > last_mod_date:
                    print("Refresh!")
                    last_mod_date = new_date
                    self.refresh()
                    self.drawSmartHome()
                pygame.display.flip()
        finally:
            pygame.quit()

if __name__ == '__main__':
    simul = Simulation()
    simul.run()
