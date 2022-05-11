import os, sys 
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150, 60)  # Set the starting position of the window. 
import pygame 
from network import Network
from buttons import * 
import offline_game 
from selection import *
from champions import * 
from Enemy_Champions import * 
from enemy_selection import * 

# Initialise pygame and font 
pygame.init()
pygame.font.init() 

# ---------------------------------Set game constants----------------------------
width = 1200
height = 720 
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

btns = [SimpleButton("Rock", 50, 500, (0,0,0)), SimpleButton("Scissors", 310, 500, (255,0,0)), SimpleButton("Paper", 180, 500, (0,255,0))]
BG = pygame.image.load("assets/menu_pic.png").convert()
# ------------------------------Game functions-----------------------------------

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def redrawWindow(win, game, p, BG, BOX, BOX_B):
    
    player_zero_champions_as_obj = [MeleeChampionOne, MeleeChampionTwo, MeleeChampionThree, RangeChampionOne]
    player_zero_champions_as_str = ["<class'champions.MeleeChampionOne'>", "<class'champions.MeleeChampionTwo'>", "<class'champions.MeleeChampionThree'>", "<class'champions.RangeChampionOne'>"]
    
    player_one_champions_as_obj = [EnemyMeleeChampionOne, EnemyMeleeChampionTwo]
    player_one_champions_as_str = ["<class'Enemy_Champions.EnemyMeleeChampionOne'>", "<class'Enemy_Champions.EnemyMeleeChampionTwo'>"]

    win.fill((128,128,128))
    
    
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        
        if p == 0:
            current_player = player_zero_champions_as_str.index(''.join(str(v) for v in game.pl_zero))
            current_player_obj = player_zero_champions_as_obj[current_player]
            # enemy_player = player_one_champions_as_str.index(''.join(str(v) for v in game.pl_one))
            # enemy_player_obj = player_one_champions_as_obj[enemy_player]
            moving_sprites = pygame.sprite.Group()
        
            ppl = current_player_obj() 
            # een = enemy_player_obj() 
            moving_sprites.add(ppl)

        elif p == 1:
            current_player = player_one_champions_as_str.index(''.join(str(v) for v in game.pl_one))
            current_player_obj = player_one_champions_as_obj[current_player]

            moving_sprites = pygame.sprite.Group()
        
            ppl = current_player_obj() 
            # een = enemy_player_obj() 
            moving_sprites.add(ppl)

        ppl.start_idle()
        # een.start_idle()

         
        # een.update()
        win.blit(BG, (0, 0))
        SCREEN.blit(BOX, (30, 480))
        SCREEN.blit(BOX_B, (480, 480))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))
        
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:  
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)
        
        moving_sprites.draw(win) 
        ppl.update()  
    pygame.display.update()

'''
main is responsible for the online part of the game and 
'''
def main():
    BG = pygame.transform.scale(pygame.image.load("assets/pixel_forest.png").convert(), (1200, 720))
    BOX = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (450, 220))
    BOX_B = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (600, 220))
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())

    if player == 0:
        x = selector()
    else: 
        x = enemy_selector()

    print("You are player", player)

    data = ("register " + f"{str(x)}")
    n.send(data) 
            
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break


        if game.bothWent():
            redrawWindow(win, game, player, BG, BOX, BOX_B)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
    
         
        redrawWindow(win, game, player, BG,  BOX, BOX_B)
        pygame.display.flip()
        pygame.display.update()


def play_offline():   # TODO: Take this out once the select champion screen is completed 
    run = True 
    x = ""
    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        win.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY win.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        win.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_OFFLINE = BaseButton(image=None, pos=(640, 390), 
                            text_input="Play offline", font=get_font(50), base_color="White", hovering_color="Green")

        PLAY_ONLINE = BaseButton(image=None, pos=(640, 480), 
                            text_input="Play online", font=get_font(50), base_color="White", hovering_color="Green")

        BACK_TO_MENU = BaseButton(image=None, pos=(640, 560), 
                            text_input="BACK to main menu", font=get_font(50), base_color="White", hovering_color="Green")
        
   
        PLAY_OFFLINE.changeColor(PLAY_MOUSE_POS)
        PLAY_OFFLINE.update(win)
        BACK_TO_MENU.changeColor(PLAY_MOUSE_POS)
        BACK_TO_MENU.update(win)
        PLAY_ONLINE.changeColor(PLAY_MOUSE_POS)
        PLAY_ONLINE.update(win)        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_OFFLINE.checkForInput(PLAY_MOUSE_POS):
                    x = selector()  # From the selector scene get the players selected champion
                    offline_game.main_menu_x(x)
                    run = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_ONLINE.checkForInput(PLAY_MOUSE_POS):
                    main() 
                    # run = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_TO_MENU.checkForInput(PLAY_MOUSE_POS):
                    return False
        pygame.display.update() 

# Options allow the player to increase or decrease the games volume. 
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        win.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS win.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        win.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = BaseButton(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")


        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return False  

        pygame.display.update()


# Menu screen that connects all screens together 
def main_menu():
    run = True 

    while run:
        win.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = BaseButton(image=None, pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#FF1212", hovering_color="#D52222")
        OPTIONS_BUTTON = BaseButton(image=None, pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#FF1212", hovering_color="#D52222")
        QUIT_BUTTON = BaseButton(image=None, pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#FF1212", hovering_color="#D52222")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_offline() 
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS): 
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


while True:
    main_menu()
