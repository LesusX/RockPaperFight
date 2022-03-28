from cgitb import text
from tabnanny import check
import pygame
import os
import sys
import random 

pygame.init()
pygame.font.init()
pygame.mixer.init()
gui_font = pygame.font.Font(None, 30)


WIDTH, HEIGHT = 1000, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Fight!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60

CHAMPION_ONE_WIDTH, CHAMPION_ONE_HEIGHT = 260, 160
CHAMPION_TWO_WIDTH, CHAMPION_TWO_HEIGHT = 500, 460
BOX_WIDTH, BOX_HEIGHT = 950, 200


FIRST_CHAMPION_IMAGE = pygame.image.load(os.path.join('Assets', 'Sprites', 'knight.png'))
FIRST_CHAMPION = pygame.transform.scale(FIRST_CHAMPION_IMAGE, (CHAMPION_ONE_WIDTH, CHAMPION_ONE_HEIGHT))

SECOND_CHAMPION_IMAGE = pygame.image.load(os.path.join('Assets', 'Sprites', 'hunter.png'))
SECOND_CHAMPION = pygame.transform.flip(pygame.transform.scale(SECOND_CHAMPION_IMAGE, (CHAMPION_TWO_WIDTH, CHAMPION_TWO_HEIGHT)), True, False)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Sprites', 'example_arena.png')), (WIDTH, HEIGHT))

BOX_IMAGE = pygame.image.load(os.path.join('Assets', 'Sprites', 'box.png'))
BOX = pygame.transform.scale(BOX_IMAGE, (BOX_WIDTH, BOX_HEIGHT))


class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.text = text 

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(WIN, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius=12)
        WIN.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.who_won()

        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

    def who_won(self): 
        choices = ["Rock", "Paper", "Scissors"]
        bot = random.choice(choices)

        if (self.text == "Rock" and bot == "Scissors") or (self.text == "Paper" and bot == "Rock") or (self.text == "Scissors" and bot == "Paper"):
            print(f"WIN! You picked {self.text}. Bot picked {bot}")
        elif (self.text == "Paper" and bot == "Scissors") or (self.text == "Rock" and bot == "Paper") or (self.text == "Scissors" and bot == "Rock"):
            print(f"DEFEAT! You picked {self.text}. Bot picked {bot}")
        else:
            print(f"Its a tie. You picked {self.text} and Bot picked {bot}")
            


button1 = Button('Rock', 120, 40, (100, 500), 5)
button2 = Button('Paper', 120, 40, (230, 500), 5)
button3 = Button('Scissors', 120, 40, (360, 500), 5)

def draw_window(red, yellow):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(BOX, (25, 440))
    WIN.blit(FIRST_CHAMPION, (yellow.x, yellow.y))
    WIN.blit(SECOND_CHAMPION, (red.x, red.y))
    button1.draw()
    button2.draw()
    button3.draw()

    pygame.display.update()


def main():
    # Crete the two places were the champion will stand 
    champion_one = pygame.Rect(500, 0, CHAMPION_ONE_WIDTH, CHAMPION_ONE_HEIGHT)
    champion_two = pygame.Rect(110, 140, CHAMPION_TWO_WIDTH, CHAMPION_TWO_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()  # By removing this you get "Pygame error: display surface quit:"

        draw_window(champion_one, champion_two)

    main()


if __name__ == "__main__":
    main()
