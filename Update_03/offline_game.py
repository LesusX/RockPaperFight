'''
Here is the offline part of the program. 
While offline, players can play against randomly generated bots and even interact with them. 
'''
import pygame, sys
from buttons import BaseButton, Button
import random 
import enemy_bot
import threading
from game import OfflineGame


pygame.init()

SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("assets/pixel_forest.png").convert(), (1200, 720))
BOX = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (450, 220))
BOX_B = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (600, 220))


font = pygame.font.Font("assets/font.ttf", 17)
posX = 5
posY = 700


def show_champ(x,y, name):
    x_name = font.render("Your champion:" + str(name), True, (255, 255, 255))
    SCREEN.blit(x_name, (x,y))



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


'''
# Ingame options 

Here the player can lower the game volume, mute the other player(chat), enable/disable BotHelper 
'''
def options():
    run = True 
    while run:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = BaseButton(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return False 

        pygame.display.update()
'''
the local assignment should be declared before we call the actuall fuck what on eaeth am I evn writting sa
I have no gain in mainstream media 
declared 

'''
def main_menu_x(pl, en):
    run = True
    enenmy_name = "Bot"

    while run:
        enemy = pygame.transform.scale(pygame.image.load(f"assets/{en}_pic.png").convert(), (150,220))
        player = pygame.transform.scale(pygame.image.load("assets/blue_pic.png").convert(), (150,220))
        dev_box = pygame.transform.scale(pygame.image.load("assets/black_pic.png").convert(), (180,80))

        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(player, (150, 220))
        SCREEN.blit(enemy, (900, 220))
        SCREEN.blit(BOX, (30, 480))
        SCREEN.blit(BOX_B, (480, 480))
        SCREEN.blit(dev_box, (10, 5))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render(f"Player  vs  {enenmy_name}", True, "#FFFFFF")
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 50))


        OPTIONS_BUTTON = BaseButton(image=None, pos=(100, 30), 
                            text_input="End Game", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        END_BUTTON = BaseButton(image=None, pos=(100, 65), 
                            text_input="QUIT", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        ROCK_BUTTON = BaseButton(image=None, pos=(130, 560), 
                            text_input="Rock", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        PAPER_BUTTON = BaseButton(image=None, pos=(130, 610), 
                            text_input="Paper", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        SCISSORS_BUTTON = BaseButton(image=None, pos=(130, 660), 
                            text_input="Scissors", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        gm = OfflineGame()
        enemy_bot = enemy_bot.Enemy()

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [OPTIONS_BUTTON, END_BUTTON, ROCK_BUTTON, PAPER_BUTTON, SCISSORS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return False 
                if ROCK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print(gm.winner_who("Rock", f"{enemy_bot.bot_move()}"))
                if PAPER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print(gm.winner_who("Paper", f"{enemy_bot.bot_move()}"))
                if SCISSORS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print(gm.winner_who("Scissors", f"{enemy_bot.bot_move()}"))
                if END_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        show_champ(posX, posY, pl)
        pygame.display.update()

