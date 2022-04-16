from pickle import NONE
from re import A 
import pygame, sys
from buttons import * 
import random 

pygame.init()
SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Champion Selection")

white = (255, 255, 255)
posX = 10
posY = 680

BG = pygame.transform.scale(pygame.image.load("assets/purple_background.png"), (1400, 790))
sel_rect_a = pygame.image.load("assets/select_rect.png")
sel_rect_b = pygame.image.load("assets/select_rect.png")
sel_rect_c = pygame.image.load("assets/select_rect.png")
font = pygame.font.Font("assets/font.ttf", 35)
sel = pygame.image.load("assets/selector.png")


def show_champ(x,y, name):
    x_name = font.render("You:" + str(name), True, (255, 255, 255))
    SCREEN.blit(x_name, (x,y))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


# Pick a random champion for the enemy bot 
# TODO: Connect this to the champion module  
def enemy():
    colours = ["orange", "pink", "red", "green", "black"]
    x = random.choice(colours)
    return x  


def selector():
    run = True 
    name = " "  
    en = " "
    while run:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(sel, (150, 80))
        SCREEN.blit(sel_rect_a, (180, 120))
        SCREEN.blit(sel_rect_b, (425, 120))
        SCREEN.blit(sel_rect_c, (640, 120))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("Select your champion", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(575, 40))

        CHAMPION_A = BaseButton(image=pygame.image.load("assets/select_rect.png"), pos=(270, 170), 
                            text_input=" ", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        
        CHAMPION_B = BaseButton(image=pygame.image.load("assets/select_rect.png"), pos=(500, 170), 
                            text_input=" ", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        
        CHAMPION_C = BaseButton(image=pygame.image.load("assets/select_rect.png"), pos=(722, 170), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        PLAY_BUTTON = BaseButton(image=None, pos=(1100, 630), 
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = BaseButton(image=None, pos=(1100, 680), 
                            text_input="Quit", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)


        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

    # TODO: add: if Play button pressed and chosen_champion != None continue else tell player to pick a champion 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    run = False  
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit() 
                if CHAMPION_A.checkForInput(MENU_MOUSE_POS):
                    chosen_champion = "A"
                    run = False 
                    name = chosen_champion
                    en = enemy()
                    return chosen_champion, en
                if CHAMPION_B.checkForInput(MENU_MOUSE_POS):
                    chosen_champion = "B"
                    run = False 
                    name = chosen_champion  
                    en = enemy()
                    return chosen_champion, en
                if CHAMPION_C.checkForInput(MENU_MOUSE_POS):
                    chosen_champion = "C"
                    run = False 
                    name = chosen_champion
                    en = enemy()
                    return chosen_champion, en
        
        show_champ(posX,posY, name)       
        pygame.display.update()