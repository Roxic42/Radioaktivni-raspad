import pygame, sys, os, warnings, time, gif_pygame
warnings.filterwarnings("ignore", category=UserWarning, message=".*iCCP.*")
pygame.init() #instalira i učitava sve pygame module

from Simulacija import * #uzmemo sve iz naše simulacije

#Definiranje displaya
WIDTH, HEIGHT = 1152, 864
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulacija radioaktivnog raspada")

#Zaključavanje FPS-a
clock = pygame.time.Clock()
FPS = 60

#Slike
MAIN_BG = pygame.image.load(os.path.join("Assets", "zelena_pozadina.jpg")).convert_alpha()
NASLOV = pygame.image.load(os.path.join("Assets", "Radioaktivni-Raspad-4-7-2024.png")).convert_alpha()

#Klasa za gumbove
class Button:
    def __init__(self, text_input, text_size, text_color, rectangle_width_and_height, rectangle_color, rectangle_hovering_color, position):
        #rectangle ispod teksta
        self.rectangle = pygame.Rect((position[0]-(rectangle_width_and_height[0]/2), position[1]-(rectangle_width_and_height[1]/2)), rectangle_width_and_height)
        self.rectangle_color, self.rectangle_hovering_color = rectangle_color, rectangle_hovering_color
        #tekst u gumbu
        self.text_input = text_input
        self.font = pygame.font.Font(None, text_size)
        self.text_surface = self.font.render(text_input, False, text_color)
        self.text_rectangle = self.text_surface.get_rect(center = self.rectangle.center)

    def update(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rectangle)
        screen.blit(self.text_surface, self.text_rectangle)

    def checkForCollision(self, mouse_position):
        if mouse_position[0] in range(self.rectangle.left, self.rectangle.right) and mouse_position[1] in range(self.rectangle.top, self.rectangle.bottom):
            return True
        return False
    
    def changeButtonColor(self):
        self.rectangle_color = self.rectangle_hovering_color

class UserInput:
    def __init__(self, naslov_text, naslov_color, pocetna_vrijednost, text_size, text_color, rectangle_width_and_height, rectangle_color, rectangle_hovering_color, position, limit):
        self.rectangle = pygame.Rect((position[0]-(rectangle_width_and_height[0]/2), position[1]-(rectangle_width_and_height[1]/2)), rectangle_width_and_height)
        self.rectangle_color, self.rectangle_hovering_color = rectangle_color, rectangle_hovering_color
        self.text_input = pocetna_vrijednost
        self.font = pygame.font.Font(None, text_size)
        self.text_color = text_color
        self.naslov_color = naslov_color
        self.update_text_surface()
        self.active = False
        self.limit = limit
        self.naslov_text = naslov_text
        self.naslov_surface = self.font.render(self.naslov_text, False, self.naslov_color)
        self.naslov_rectangle = self.naslov_surface.get_rect(left=self.rectangle.left, top=self.rectangle.top - text_size)

    def update_text_surface(self):
        self.text_surface = self.font.render(self.text_input, False, self.text_color)
        self.text_rectangle = self.text_surface.get_rect(left=self.rectangle.left + 10, centery=self.rectangle.centery)

    def update(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rectangle)
        screen.blit(self.text_surface, self.text_rectangle)
        screen.blit(self.naslov_surface, self.naslov_rectangle)

    def changeButtonColor(self, mouse_position):
        if self.active:
            self.rectangle_color = self.rectangle_hovering_color
        elif self.rectangle.collidepoint(mouse_position):
            self.rectangle_color = self.rectangle_hovering_color
        else:
            self.rectangle_color = (0, 0, 0)

    def handle_eventove(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text_input) < self.limit:
                self.text_input += event.unicode
            self.text_surface = self.font.render(self.text_input, False, self.text_color)

def escape_screen():
    transparent_background = pygame.Surface((WIDTH, HEIGHT))
    transparent_background.fill("Black")
    transparent_background.set_alpha(120)
    SCREEN.blit(transparent_background, (0,0))
    while True:
        box = pygame.Surface((400, 300))
        box.fill("Gray")
        SCREEN.blit(box, (376, 300))
        naslov_font = pygame.font.Font(None, 35)
        naslov_surface = naslov_font.render("Želite li izaći iz simulacije?", False, "Black")
        naslov_rectangle = naslov_surface.get_rect(topleft = (424, 310))
        SCREEN.blit(naslov_surface, naslov_rectangle)

        DA = Button("DA", 35, "White", (200, 75), "Black", "Red", (576,430))
        NE = Button("NE", 35, "White", (200, 75), "Black", "Green", (576,530))
        mouse_position = pygame.mouse.get_pos()

        for gumb in [DA, NE]:
            if gumb.checkForCollision(mouse_position):
                gumb.changeButtonColor()
            gumb.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DA.checkForCollision(mouse_position):
                    return True
                if NE.checkForCollision(mouse_position):
                    return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        pygame.display.update()
        clock.tick(FPS)


def main():
    if os.path.exists("graf.gif"):
        os.remove("graf.gif")
    else:
        pass
    while True:
        SCREEN.fill("Black")
        mouse_position = pygame.mouse.get_pos()
        SCREEN.blit(MAIN_BG, (0,0))
        SCREEN.blit(NASLOV, (75,0))

        DALJE_GUMB = Button("DALJE", 35, "White", (200, 100), "Black", "Gray", (576,500))
        IZADI_GUMB = Button("IZAĐI", 35, "White", (200, 100), "Black", "Gray", (576,650))
        for gumb in [DALJE_GUMB, IZADI_GUMB]:
            if gumb.checkForCollision(mouse_position):
                gumb.changeButtonColor()
            gumb.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if escape_screen():
                        pygame.quit()
                        sys.exit()
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DALJE_GUMB.checkForCollision(mouse_position):
                    if namjestanje_screen():
                        break
                    if simulacija():
                        break
                if IZADI_GUMB.checkForCollision(mouse_position):
                    pygame.quit
                    sys.exit()
                pass
        pygame.display.update()
        clock.tick(FPS)

def namjestanje_screen():
    global pocetni_N, vrijeme, pol_raspad
    pocetni_N = 1600
    vrijeme = 150
    pol_raspad = 20
    if os.path.exists("graf.gif"):
        os.remove("graf.gif")
    else:
        pass
    POCETNI = UserInput("Početni broj atoma:", "Black",f"{pocetni_N}", 40, "white", (100, 50), "Black", "Green", (176,200), 5)
    VRIJEME = UserInput("Vrijeme trajanja simulacije [s]:", "Black",f"{vrijeme}", 40, "white", (100, 50), "Black", "Green", (176,300), 5)
    POLURASPAD = UserInput("Vrijeme poluraspada [s]:", "Black",f"{pol_raspad}", 40, "white", (100, 50), "Black", "Green", (176,400), 5)
    naslov_font = pygame.font.Font(None, 100)
    naslov_surface = naslov_font.render("NAMJESTI VARIJABLE", False, "Black")
    naslov_rectangle = naslov_surface.get_rect(topleft = (50, 20))
    while True:
        SCREEN.fill("#C1E1C1")
        SCREEN.blit(naslov_surface, naslov_rectangle)
        mouse_position = pygame.mouse.get_pos()

        RASPADNI = Button("Raspadni element", 40, "White", (300, 100), "Black", "Gray", (976,800))

        for gumb in [RASPADNI]:
            if gumb.checkForCollision(mouse_position):
                gumb.changeButtonColor()
            gumb.update(SCREEN)

        for event in pygame.event.get():
            POLURASPAD.handle_eventove(event)
            if not POLURASPAD.active:
                pol_raspad = int(POLURASPAD.text_input)
            VRIJEME.handle_eventove(event)
            if not VRIJEME.active:
                vrijeme = int(VRIJEME.text_input)
            POCETNI.handle_eventove(event)
            if not POCETNI.active:
                pocetni_N = int(POCETNI.text_input)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if escape_screen():
                        pygame.quit()
                        sys.exit()
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RASPADNI.checkForCollision(mouse_position):
                    if simulacija():
                        break
                pass


        for gumb in [POCETNI, VRIJEME, POLURASPAD]:
            gumb.changeButtonColor(mouse_position)
            gumb.update(SCREEN)

        pygame.display.update()
        clock.tick(FPS)

def simulacija():
    global pocetni_N, vrijeme, pol_raspad
    if os.path.exists("graf.gif"):
        os.remove("graf.gif")
    else:
        pass
    element = RadioaktivniMaterijal(pocetni_N, vrijeme, pol_raspad=pol_raspad)
    print(f"{element.pocetni_N}, {element.vrijeme}, {element.pol_raspad}")
    element.raspadni()
    GRAF = gif_pygame.load("graf.gif")
    text_font = pygame.font.Font(None, 30)
    preostali_surface = text_font.render(f"BROJ PREOSTALIH ATOMA: {element.preostali_N}", False, "Black")
    preostali_rectangle = preostali_surface.get_rect(topleft = (700, 100))
    raspadnuti_surface = text_font.render(f"BROJ RASPADNUTIH ATOMA: {element.raspadnuti_N}", False, "Black")
    raspadnuti_rectangle = raspadnuti_surface.get_rect(topleft = (700, 150))
    while True:
        SCREEN.fill("#C1E1C1")
        SCREEN.blit(raspadnuti_surface, raspadnuti_rectangle)
        SCREEN.blit(preostali_surface, preostali_rectangle)
        mouse_position = pygame.mouse.get_pos()
        GRAF.render(SCREEN, (50,50))

        RASPADNI = Button("Ponovo namjesti varijable", 40, "White", (400, 100), "Black", "Gray", (976,800))

        for gumb in [RASPADNI]:
            if gumb.checkForCollision(mouse_position):
                gumb.changeButtonColor()
            gumb.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if escape_screen():
                        pygame.quit()
                        sys.exit()
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RASPADNI.checkForCollision(mouse_position):
                    if namjestanje_screen():
                        break
                pass

        pygame.display.update()
        clock.tick(FPS)



if __name__ == "__main__":
    main()