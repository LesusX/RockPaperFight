import os, sys
from tkinter.messagebox import YESNO 
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150, 60)  # Set the starting position of the window. 
import pygame 
from network import Network
from buttons import * 
import offline_game 
import random 
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

# Store all class objects on lists and then sort our based on the player selection, from selection screen. 
# Based on the players choice find the matching object and then convert it in a string that can be later on sent on the server. With tthat string create objects. 
# TODO: Fix network and server so that they can handle direct objects instead of strings. 
player_zero_champions_as_obj = [MeleeChampionOne, MeleeChampionTwo, MeleeChampionThree, MeleeChampionFour, MeleeChampionFive, MeleeChampionSix, MeleeChampionSeven, MeleeChampionEight, MeleeChampionNine, MeleeChampionTen, MeleeChampionEleven]
player_zero_champions_as_str = ["<class'champions.MeleeChampionOne'>", "<class'champions.MeleeChampionTwo'>", "<class'champions.MeleeChampionThree'>", "<class'champions.MeleeChampionFour'>",
"<class'champions.MeleeChampionFive'>", "<class'champions.MeleeChampionSix'>", "<class'champions.MeleeChampionSeven'>", "<class'champions.MeleeChampionEight'>",  "<class'champions.MeleeChampionNine'>", "<class'champions.MeleeChampionTen'>", "<class'champions.MeleeChampionEleven'>"]
player_one_champions_as_obj = [EnemyMeleeChampionOne, EnemyMeleeChampionTwo, EnemyMeleeChampionThree, EnemyMeleeChampionFour, EnemyMeleeChampionFive,
EnemyMeleeChampionSix, EnemyMeleeChampionSeven, EnemyMeleeChampionEight, EnemyMeleeChampionNine, EnemyMeleeChampionTen, EnemyMeleeChampionEleven]
player_one_champions_as_str = ["<class'Enemy_Champions.EnemyMeleeChampionOne'>", "<class'Enemy_Champions.EnemyMeleeChampionTwo'>", 
"<class'Enemy_Champions.EnemyMeleeChampionThree'>", "<class'Enemy_Champions.EnemyMeleeChampionFour'>", "<class'Enemy_Champions.EnemyMeleeChampionFive'>",
"<class'Enemy_Champions.EnemyMeleeChampionSix'>", "<class'Enemy_Champions.EnemyMeleeChampionSeven'>", "<class'Enemy_Champions.EnemyMeleeChampionEight'>",
"<class'Enemy_Champions.EnemyMeleeChampionNine'>", "<class'Enemy_Champions.EnemyMeleeChampionTen'>", "<class'Enemy_Champions.EnemyMeleeChampionEleven'>"]

arenas = ["Forest", "Ice", "Cave", "Desert"]

arena_type = random.choice(arenas) 

MENU_BACKGROUND = pygame.image.load("assets/menu_pic.png").convert()                                           # TODO: Fix the background and bonusses on the servers side.
BG = pygame.transform.scale(pygame.image.load(f"assets/arenas/{arena_type}_arena.png").convert(), (1200, 720)) # Set a random bg, so it easy to tell if the window represents player zero or player one
BOX = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (450, 220))
BOX_B = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (600, 220))

# Game variables related to moves, and the available potions
move_list = [] 
pl_zero_potion_count = 2 
pl_one_potion_count = 2 

# Create the blue highlighted parts of the buttons and store them in a list 
button1 = Button('Rock',130, 40,(65, 550),5)
button2 = Button('Paper',130, 40,(65, 600),5)
button3 = Button('Scissors',170, 40,(45, 650),5)
button4 = Button('Lock',170, 50,(280, 550),5)
btns = [button1, button2, button3, button4]

# ------------------------------Game functions-----------------------------------
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# Function that extents the main while loop of the game 
def redrawWindow(win, game, p, BG, BOX, BOX_B, moving_sprites, champion_zero, champion_one, game_btn, MENU_MOUSE_POS, btns):
    win.fill((128,128,128))
    
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        win.blit(BG, (0, 0))
        SCREEN.blit(BOX, (30, 480))
        SCREEN.blit(BOX_B, (480, 480))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Your Move", 1, (0, 255,0))
        win.blit(text, (550, 560))

        text = font.render("Opponents", 1, (0, 255, 0))
        win.blit(text, (760, 560))
        # Depending on each players move. Show the status to the player. 
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
            win.blit(text2, (560, 600))
            win.blit(text1, (770, 600))
        else:
            win.blit(text1, (560, 600))
            win.blit(text2, (770, 600))
             
        button1.draw() 
        button2.draw() 
        button3.draw() 
        button4.draw() 

        # Get a hold of all available buttons and render them 
        for button in game_btn:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        champion_zero.update() # Use the update comand so that animations can be switched in real time without lag 
        champion_one.update()  
        moving_sprites.draw(win) 
    pygame.display.flip()

'''
main is responsible for the online part of the game and 
'''
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())

    # Depending on who logs in online for a game show either selector or enemy_selector
    # Enemy selector places characters on the right of the scrchampion_onewhile the other one renders them on the left 
    if player == 0:
        x = selector()
    else: 
        x = enemy_selector()

    # Sent the chosen champion from the selector to the server and register the users choice 
    data = ("register " + f"{str(x)}")
    n.send(data) 
    
    # Creates a group were all animated sprtes can be stored in 
    moving_sprites = pygame.sprite.Group()
    champion_zero = x()  # Since both Enemy champions and normal champions are called. Take the users choice and let the program create an object based on the choice. 
    moving_sprites.add(champion_zero) # Add users champion on a sprite grupp so it can be rendered later on 

    # Within this loop the game is waiting for another player to connect on a game. 
    # When two people are in a room and both of them to picked a champion, break and start the game
    loop = True 
    while loop:
        win.fill((128,128,128))
        game = n.send("get") # Always get the game data from the server 

        # The player that creates a game has id:0 
        # Once a player with id:1 joins the game take the string representing their choice and match it with the enemy champion class object 
        # The champion class objects are ment to be rendered on the left of the scrchampion_onewhile enemy champions are rendered on the right. 
        # Both Enemy champions and normal champions are the same. 
        if player == 0 and game.both_chose():
            enemy_player = player_one_champions_as_str.index(''.join(str(v) for v in game.pl_one))
            enemy_player_obj = player_one_champions_as_obj[enemy_player]
            champion_one= enemy_player_obj()
            moving_sprites.add(champion_one)
            loop = False 
        # If the player joins an already created game take the users champion and render it on the right side of the screen. 
        elif player == 1 and game.both_chose():
            enemy_player = player_zero_champions_as_str.index(''.join(str(v) for v in game.pl_zero))
            enemy_player_obj = player_zero_champions_as_obj[enemy_player]
            champion_one= enemy_player_obj()
            moving_sprites.add(champion_one)
            loop = False 
        else: # If there is only one player in wait 
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Waiting for Player...", 1, (255,0,0), True)
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
    
        pygame.display.update()

    # Activate the idle animation for both champion_one(player 1) and champion_zero(player0) champions 
    champion_one.start_idle() 
    champion_zero.start_idle()

# Game's main loop 
    while run:
        clock.tick(30) # -------------- ------ ----- ----- ----- ----
        try: # Constantly ask for the game 
            game = n.send("get")
        except: # If the connection is disturbed, disconnect from server and return on menu scrchampion_one
            run = False
            print("Couldn't get game")
            break

        # Get a hold of the muse's position every time
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Create the buttons and store them in a list 
        ROCK_BUTTON = BaseButton(image=None, pos=(130, 560), 
                            text_input="Rock", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        PAPER_BUTTON = BaseButton(image=None, pos=(130, 610), 
                            text_input="Paper", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        SCISSORS_BUTTON = BaseButton(image=None, pos=(130, 660), 
                            text_input="Scissors", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        ULT_ATTACK_BUTTON = BaseButton(image=None, pos=(360, 660), 
                            text_input="Ult", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        LOCK_BUTTON = BaseButton(image=None, pos=(360, 560), 
                            text_input="LOCK MOVE", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        game_btn = [ROCK_BUTTON, PAPER_BUTTON, SCISSORS_BUTTON, LOCK_BUTTON, ULT_ATTACK_BUTTON] 

        # Run only if both playes picked a choice.
        if game.bothWent():
            # First update the scrchampion_onein order to show the results
            redrawWindow(win, game, player, BG, BOX, BOX_B, moving_sprites, champion_zero, champion_one, game_btn, MENU_MOUSE_POS, btns) 
            try: # Always get the game and check if both players are still conected! 
                game = n.send("reset")
            except:
                run = False # If the connection breaks then reset the game. 
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
                print("YOU WON THIS ROUND!") # Use this line to check if everything works. The animations are buggy and the results can't be schampion_one80% of the times
                pygame.display.update()
                pygame.time.delay(2000)
                champion_zero.start_running() 

            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
                print("TIE GAME! NO WINNERS!") # Use this line to check if everything works. The animations are buggy and the results can't be schampion_one80% of the times
                pygame.display.update()
                pygame.time.delay(2000)
                move_list.clear() 
                n.send("reset_buttons") 
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
                print("YOU LOST THIS ROUND") # Use this line to check if everything works. The animations are buggy and the results can't be schampion_one80% of the times
                pygame.display.update()
                pygame.time.delay(2000)
                champion_one.start_running()

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

        for event in pygame.event.get(): # Check for any events 
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                if player == 0 and game.pl_zero_buttons_locked == False:
                    # Let the player click the button and save the move of the button on a temporary list 
                    # If later on the player clicks lock save the temporary move as permanent for the round  
                    if ROCK_BUTTON.checkForInput(MENU_MOUSE_POS) and not game.p1Went: 
                        move_list.clear() 
                        move_list.append("Rock") 
                        for btn in btns:      
                            if btn != button1:                                       
                                btn.is_locked = False                                


                    if PAPER_BUTTON.checkForInput(MENU_MOUSE_POS) and not game.p1Went:
                        move_list.clear()
                        move_list.append("Paper")  
                        for btn in btns:
                            if btn != button2:
                                btn.is_locked = False 

                    if SCISSORS_BUTTON.checkForInput(MENU_MOUSE_POS) and not game.p1Went:
                        move_list.clear() 
                        move_list.append("Scissors")           
                        for btn in btns:
                            if btn != button3:
                                btn.is_locked = False 

                    # if Player clicks on lock button for the first time. Save the selected move from above and tell the game that the player chose a move 
                    if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and move_list and game.p1Went == False:
                        n.send(move_list[0])

                    # If Player has a locked move and clicks then say "You chose a move "
                    if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and game.p1Went == True:
                        button4.is_locked = True  

                    # If Player has a locked move and clicks then say "You chose a move "
                    if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and game.p1Went == False:
                        button4.is_locked = False  

                if player == 1 and game.pl_one_buttons_locked == False:
                    # Let the player click the button and save the move on a temporary list 
                    # If later on the player clicks lock save the temporary move as permanent for the round  
                    if ROCK_BUTTON.checkForInput(MENU_MOUSE_POS) and not game.p2Went: 
                        move_list.clear() 
                        move_list.append("Rock") 
                        for btn in btns:      
                            if btn != button1:                                       
                                btn.is_locked = False                                

                    if PAPER_BUTTON.checkForInput(MENU_MOUSE_POS) and not game.p2Went:
                        move_list.clear()
                        move_list.append("Paper")  
                        print(move_list[0])                             
                        for btn in btns:
                            if btn != button2:
                                btn.is_locked = False 

                    if SCISSORS_BUTTON.checkForInput(MENU_MOUSE_POS) and not game.p2Went:
                        move_list.clear() 
                        move_list.append("Scissors")           
                        for btn in btns:
                            if btn != button3:
                                btn.is_locked = False 

                    # if Player clicks on lock button for the first time. Save the selected move from above and tell the game that the player chose a move 
                    if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and move_list and game.p2Went == False:
                        n.send(move_list[0])

                    # If Player has a locked move and clicks then say "You chose a move "
                    if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and (game.p2Went == True):
                        button4.is_locked = True  # TODO: Blit the move on the scrchampion_one


                    # If Player has a locked move and clicks then say "You chose a move "
                    if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and (game.p2Went == False):
                        button4.is_locked = False  # TODO: Blit on Scrchampion_onethat the player chose a move and now has to wait 

        # Checks when the attack is done and when it lands. Then clears all buttons and choices 
        if move_list and champion_one.attack_done == True:
            n.send("reset_buttons")
            move_list.clear()
            for btn in btns:
                btn.is_locked = False 

        if move_list and champion_zero.attack_done == True:
            n.send("reset_buttons")
            move_list.clear() 
            for btn in btns:
                btn.is_locked = False 
        
        if move_list and champion_zero.attack_landed == True:
            champion_one.health -= 12 
            champion_one.get_damage(120)

        if move_list and champion_one.attack_landed == True:
            champion_zero.health -= 12
            champion_zero.get_damage(120)

        # -----------------------------------------------------------------------------
        # Once either of the player's champion is dead, end the game with a loading scrchampion_oneand return them to the main menu
        if champion_one.health <= 0: 
            pl_zero_potion_count = 2 
            pl_one_potion_count = 2 
            start_loading_screen()
            return False   

        if champion_zero.health <= 0:
            pl_zero_potion_count = 2 
            pl_one_potion_count = 2 
            start_loading_screen()
            return False
         
        redrawWindow(win, game, player, BG,  BOX, BOX_B, moving_sprites, champion_zero, champion_one, game_btn, MENU_MOUSE_POS, btns) 
        pygame.display.flip()  # By using display.flip there is no animation lag but the performance might vary


def play_offline():   # TODO: Take this out once the select champion scrchampion_oneis completed and stable!
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        win.fill("black")
        # Window buttons 
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

# Options allow the player to increase or decrease the games volume, dificulty level and even brightness 
# TODO: Add the above functionalities 
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        win.fill("white")

        OPTIONS_TEXT = get_font(30).render("This is the OPTIONS win! ", True, "Black")
        OPTIONS_TEXT_TWO = get_font(30).render("There are no options available...Yet!", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        win.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_RECT = OPTIONS_TEXT_TWO.get_rect(center=(640, 300))
        win.blit(OPTIONS_TEXT_TWO, OPTIONS_RECT)

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

# Menu scrchampion_onethat connects all screens together 
def main_menu():
    while True:
        win.blit(MENU_BACKGROUND, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(65).render("Rock Paper Fight!", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 100))

        # Create some buttons for the main menu screen. 
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

# Always keep the menu on while the game is running.
while True:
    main_menu()
