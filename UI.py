import pygame, sys, os, warnings, time #,pygamepopup
warnings.filterwarnings("ignore", category=UserWarning, message=".*iCCP.*")
pygame.init() #instalira i učitava sve pygame module
#pygamepopup.init()

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
        self.player_number = 0

    def update(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rectangle)
        screen.blit(self.text_surface, self.text_rectangle)

    def checkForCollision(self, mouse_position):
        if mouse_position[0] in range(self.rectangle.left, self.rectangle.right) and mouse_position[1] in range(self.rectangle.top, self.rectangle.bottom):
            return True
        return False
    
    def changeButtonColor(self):
        self.rectangle_color = self.rectangle_hovering_color

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

class Slider:
    def __init__(self, pos:tuple, size:tuple, initial_val:float, min:int, max:int):
        self.pos = pos
        self.size = size

        self.slider_left = self.pos[0] - (size[0]//2)
        self.slider_right = self.pos[0] + (size[0]//2)
        self.slider_top = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right - self.slider_left)*initial_val #u postotcima

        self.rect = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.gumb_rect = pygame.Rect(self.slider_left + self.initial_val - 5, self.slider_top, 10, self.size[1])

    def move_slider(self, mouse_pos):
        self.gumb_rect.centerx = mouse_pos[0]

    def render(self, SCREEN):
        pygame.draw.rect(SCREEN, "dark grey", self.rect)
        pygame.draw.rect(SCREEN, "blue  ", self.gumb_rect)


element = RadioaktivniMaterijal(1600, 100, pol_raspad=20)
def main():
    global element
    while True:
        SCREEN.fill("Black")
        mouse_position = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        SCREEN.blit(MAIN_BG, (0,0))
        SCREEN.blit(NASLOV, (75,0))

        kliznica = Slider((576,800), (100, 30), 0.5, 0, 100)
        DALJE_GUMB = Button("DALJE", 35, "White", (200, 100), "Black", "Gray", (576,500))
        IZADI_GUMB = Button("IZAĐI", 35, "White", (200, 100), "Black", "Gray", (576,650))
        for gumb in [DALJE_GUMB, IZADI_GUMB]:
            if gumb.checkForCollision(mouse_position):
                gumb.changeButtonColor()
            gumb.update(SCREEN)

        for slider in [kliznica]:
            if slider.rect.collidepoint(mouse_position) and mouse[0]:
                slider.move_slider(mouse_position)
            slider.render(SCREEN)

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
    while True:
        SCREEN.fill("#C1E1C1")
        mouse_position = pygame.mouse.get_pos()


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
                pass

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()