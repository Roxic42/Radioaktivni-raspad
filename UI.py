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
GRAF = gif_pygame.load("graf.gif")

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
    def __init__(self, text_size, text_color, rectangle_width_and_height, rectangle_color, rectangle_hovering_color, position):
        self.rectangle = pygame.Rect((position[0]-(rectangle_width_and_height[0]/2), position[1]-(rectangle_width_and_height[1]/2)), rectangle_width_and_height)
        self.rectangle_color, self.rectangle_hovering_color = rectangle_color, rectangle_hovering_color
        self.text_input = ""
        self.font = pygame.font.Font(None, text_size)
        self.text_color = text_color
        self.update_text_surface()
        self.active = False

    def update_text_surface(self):
        self.text_surface = self.font.render(self.text_input, False, self.text_color)
        self.text_rectangle = self.text_surface.get_rect(left=self.rectangle.left + 30, centery=self.rectangle.centery)

    def update(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rectangle)
        screen.blit(self.text_surface, self.text_rectangle)

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
            elif len(self.text_input) < 2:
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

element = RadioaktivniMaterijal(1600, 100, pol_raspad=20)
def main():
    global element
    while True:
        SCREEN.fill("Black")
        mouse_position = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
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
                    if simulacija():
                        break
                if IZADI_GUMB.checkForCollision(mouse_position):
                    pygame.quit
                    sys.exit()
                pass
        pygame.display.update()
        clock.tick(FPS)

def simulacija():
    POLURASPAD = UserInput(40, "White", (200, 100), "Black", "Gray", (576,500))
    while True:
        SCREEN.fill("#C1E1C1")
        GRAF.render(SCREEN, (50,50))
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            POLURASPAD.handle_eventove(event)
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
                pass

        for gumb in [POLURASPAD]:
            gumb.changeButtonColor(mouse_position)
            gumb.update(SCREEN)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()