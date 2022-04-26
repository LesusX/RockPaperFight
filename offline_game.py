'''
Here is the offline part of the program. 
While offline, players can play against randomly generated bots and even interact with them. 
'''
import time 
import pygame, sys
from buttons import BaseButton, Button
import random 
from game import OfflineGame
import enemy_bot
import threading 

pygame.init()

SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Menu")
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
Use redraw_win to clean the main while loop on man_menu_x
'''
def redraw_win(SCREEN, BG, player, enemy, BOX, BOX_B, dev_box, time, MENU_TEXT, MENU_RECT, game_obj):
    SCREEN.blit(BG, (0, 0))
    SCREEN.blit(player, (150, 200))
    SCREEN.blit(enemy, (900, 220))
    SCREEN.blit(BOX, (30, 480))
    SCREEN.blit(BOX_B, (480, 480))
    SCREEN.blit(dev_box, (10, 5))
    SCREEN.blit(time, (15,90))
    SCREEN.blit(MENU_TEXT, MENU_RECT)
    
    if game_obj.both_played():
        print(f"You: {game_obj.player_move[0]}, Enemy: {game_obj.enemy_move[0]}!")
        print(game_obj.winner_who(game_obj.player_move[0], game_obj.enemy_move[0]))
        game_obj.reset_moves()
    
'''
the local assignment should be declared before we call the actuall fuck what on eaeth am I evn writting sa
I have no gain in mainstream media 
declared 
'''
def main_menu_x(pl):
    run = True
    # Create the Enemy Bot 
    en_bot = enemy_bot.Enemy()
    colour = en_bot.bot_color()
    en_bot_name = en_bot.name
    game_obj = OfflineGame()
    
    # Time variables 
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks() #starter tick
    minutes_played = 0 

    # Objects that will be shown on the screen 
    enemy = pygame.transform.scale(pygame.image.load(f"assets/{colour}_pic.png").convert(), (150,220))
    player = pygame.transform.scale(pygame.image.load("assets/blue_pic.png").convert(), (150,220))
    dev_box = pygame.transform.scale(pygame.image.load("assets/black_pic.png").convert(), (190,110))
    BG = pygame.transform.scale(pygame.image.load("assets/pixel_forest.png").convert(), (1200, 720))
    BOX = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (450, 220))
    BOX_B = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (600, 220))    
    enemy = pygame.transform.scale(pygame.image.load(f"assets/{colour}_pic.png").convert(), (150,220))
    player = pygame.transform.scale(pygame.image.load("assets/blue_pic.png").convert(), (150,220))
    dev_box = pygame.transform.scale(pygame.image.load("assets/black_pic.png").convert(), (190,110))
    MENU_TEXT = get_font(50).render(f"Player  vs  {en_bot_name}", True, "#FFFFFF")
    MENU_RECT = MENU_TEXT.get_rect(center=(600, 50))

    while run:
        clock.tick(60)

        # Time related variables 
        seconds = int((pygame.time.get_ticks()-start_ticks)/1000) #calculate how many seconds
        time = font.render("Time: " + str(f"{minutes_played}:{seconds}"), True, (255, 255, 255))
        if seconds == 60:
            start_ticks = pygame.time.get_ticks()
            minutes_played += 1

        if seconds % 5 == 0 and not game_obj.is_locked:
            x = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
            print(random.choice(x))
            game_obj.lock_timer(is_locked=True)
        if seconds % 5 != 0 and game_obj.is_locked:
            game_obj.lock_timer(is_locked=False)


        redraw_win(SCREEN, BG, player, enemy, BOX, BOX_B, dev_box, time, MENU_TEXT, MENU_RECT, game_obj)
        show_champ(posX, posY, pl)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Create the buttons 
        QUIT_GAME_BUTTON = BaseButton(image=None, pos=(100, 30), 
                            text_input="End Game", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        END_BUTTON = BaseButton(image=None, pos=(100, 65), 
                            text_input="QUIT", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        ROCK_BUTTON = BaseButton(image=None, pos=(130, 560), 
                            text_input="Rock", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        PAPER_BUTTON = BaseButton(image=None, pos=(130, 610), 
                            text_input="Paper", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        SCISSORS_BUTTON = BaseButton(image=None, pos=(130, 660), 
                            text_input="Scissors", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        LOCK_BUTTON = BaseButton(image=None, pos=(400, 560), 
                            text_input="LOCK MOVE", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
           
        for button in [QUIT_GAME_BUTTON, END_BUTTON, ROCK_BUTTON, PAPER_BUTTON, SCISSORS_BUTTON, LOCK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_GAME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return False 


                if ROCK_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played:
                    game_obj.set_player_movement("Rock", False)
                    # print(f"{game_obj.temporary_move[0]} clicked!")

                if PAPER_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played:
                    game_obj.set_player_movement("Paper", False)
                    # print(f"{game_obj.temporary_move[0]} clicked!")

                if SCISSORS_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played:
                    game_obj.set_player_movement("Scissors", False)
                    # print(f"{game_obj.temporary_move[0]} clicked!")


                if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and game_obj.temporary_move and (game_obj.player_played == False):
                    game_obj.set_player_movement(game_obj.temporary_move[0], True)
                    game_obj.get_enemy_move(enemy_played=True)
                    # print(f"You just picked: {game_obj.player_move[0]}")
                
                if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and (game_obj.player_played == True):
                    pass # TODO: for 1-3 seconds print on screen that move is locked
                    # print(f"You already picked: {game_obj.player_move[0]}")

                if END_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    run = False
                    sys.exit()

        
        pygame.display.update()