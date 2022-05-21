'''
Here is the offline part of the program. 
While offline, players can play against randomly generated bots and even interact with them. 
'''
import random
import pygame, sys
from buttons import * 
from game import OfflineGame
import enemy_bot
from loading_screen import * 

# Basic for starting pygame properly 
pygame.init()
SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Menu")
font = pygame.font.Font("assets/font.ttf", 17)


# Use PosX, posY to set the position of the chosen champions name 
posX = 5
posY = 700
arenas = ["forest", "ice", "cave", "desert"]

move_list = []

# Show the name of the players chosen champion 
def show_champ(x,y, name):
    x_name = font.render("Your champion:" + str(name), True, (255, 255, 255))
    SCREEN.blit(x_name, (x,y))

# Get the font that will be used for all text in the game 
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
def redraw_win(SCREEN, BG, BOX, BOX_B, dev_box, time, MENU_TEXT, MENU_RECT, moving_sprites, button1, button2, button3, button4):
    SCREEN.blit(BG, (0, 0))
    SCREEN.blit(BOX, (30, 480))
    SCREEN.blit(BOX_B, (480, 480))
    button1.draw() 
    button2.draw() 
    button3.draw() 
    button4.draw() 
    SCREEN.blit(dev_box, (10, 5))
    SCREEN.blit(time, (15,90))
    SCREEN.blit(MENU_TEXT, MENU_RECT)
    moving_sprites.draw(SCREEN)


def fps():
    fr = "V.3 Fps: " + str(int(clock.get_fps()))
    frt = font.render(fr, 1, pygame.Color("white"))
    return frt

# TODO: Join Button with Base button to reduce code 
button1 = Button('Rock',130, 40,(65, 550),5)
button2 = Button('Papper',130, 40,(65, 600),5)
button3 = Button('Scissors',170, 40,(45, 650),5)
button4 = Button('Lock',170, 50,(280, 550),5)

btns = [button1, button2, button3, button4]
potion_count = 2

def main_menu_x(pl):
    global clock
    # Create the Enemy Bot 
    en_bot = enemy_bot.Enemy()
    q = en_bot.pick_champion() 
    en_bot_name = en_bot.name

    game_obj = OfflineGame("MARTHA", f"{en_bot_name}")  
    run = True 
    # Champions objects 
    # Get the name of the selected champions subcless and create an object to be used on this game.
    # The positions of the characters are fixed in the champions file 
    moving_sprites = pygame.sprite.Group()
    ppl = pl() 
    een = q()
    moving_sprites.add(ppl, een) 

    # TODO: Create the enemy from the other file and bring it here.
    # cut lines in half 
    print(f" The enemy  picked: {een.name} \nYou picked {ppl.name}")
    
    # Time variables 
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks() # Let pygame count the ticks for time 
    minutes_played = 0 

    arena_type = random.choice(arenas) 

    # Objects that will be shown on the screen 
    dev_box = pygame.transform.scale(pygame.image.load("assets/black_pic.png").convert(), (190,110))
    BG = pygame.transform.scale(pygame.image.load(f"assets/arenas/{arena_type}_arena.png").convert(), (1200, 720))
    BOX = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (450, 220))
    BOX_B = pygame.transform.scale(pygame.image.load("assets/input_box.png").convert(), (600, 220))    
    dev_box = pygame.transform.scale(pygame.image.load("assets/black_pic.png").convert(), (190,110))
    MENU_TEXT = get_font(20).render(f"{ppl.name}  vs  {een.name}", True, "#FFFFFF")
    MENU_RECT = MENU_TEXT.get_rect(center=(600, 50))

    # Start the idle before the loop so it doesn't block the updates 
    ppl.start_idle()
    een.start_idle()
    while run:
        clock.tick(60)  

        # Time related variables 
        seconds = int((pygame.time.get_ticks()-start_ticks)/1000) #calculate how many seconds
        time = font.render("Time: " + str(f"{minutes_played}:{seconds}"), True, (255, 255, 255))

        # Every 60 seconds add 1 minute on the timer and restart the pygame timer to count again all seconds from 0-60 
        if seconds == 60:
            start_ticks = pygame.time.get_ticks()
            minutes_played += 1

        '''
        # Every x seconds let the enemy say something to the player 
        if seconds % 15 == 0 and game_obj.can_bot_talk:
            print(en_bot.bot_chater()) # TODO: Add a text box and print the reply there- 
            game_obj.lock_timer(can_bot_talk=False)
        if seconds % 15 != 0 and not game_obj.can_bot_talk:
            game_obj.lock_timer(can_bot_talk=True)
        '''

        # For better organisation place here things tha must be rendered on the screen 
        redraw_win(SCREEN, BG, BOX, BOX_B, dev_box, time, MENU_TEXT, MENU_RECT, moving_sprites, button1, button2, button3, button4)
        show_champ(posX, posY, ppl.name)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Create the buttons 
        QUIT_GAME_BUTTON = BaseButton(image=None, pos=(100, 30), 
                            text_input="End Game", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        END_BUTTON = BaseButton(image=None, pos=(100, 65), 
                            text_input="QUIT", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        ROCK_BUTTON = BaseButton(image=None, pos=(130, 560), 
                            text_input="Rock", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        PAPPER_BUTTON = BaseButton(image=None, pos=(130, 610), 
                            text_input="Paper", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        SCISSORS_BUTTON = BaseButton(image=None, pos=(130, 660), 
                            text_input="Scissors", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        HEAL_BUTTON = BaseButton(image=None, pos=(360, 610), 
                            text_input="Heal", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        ULT_ATTACK_BUTTON = BaseButton(image=None, pos=(360, 660), 
                            text_input="Ult", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")
        

        LOCK_BUTTON = BaseButton(image=None, pos=(360, 560), 
                            text_input="LOCK MOVE", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        # Get a hold of all available buttons and render them 
        for button in [QUIT_GAME_BUTTON, END_BUTTON, ROCK_BUTTON, PAPPER_BUTTON,
        SCISSORS_BUTTON, LOCK_BUTTON, HEAL_BUTTON, ULT_ATTACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game_obj.game_buttons_locked == False:
                if QUIT_GAME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return False 

                # Let the player click the button and save the move of the button on a temporary list 
                # If later on the player clicks lock save the temporary move as permanent for the round  
                if ROCK_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played: 
                    move_list.clear() 
                    move_list.append(button1)                                             
                    for btn in btns:                                            # players movements and register´temporary move. 
                        game_obj.set_player_movement(f"{button1.text}", False)   # Call the game function responsible for the 
                        if btn != button1:                                       
                            btn.is_locked = False                                

                if HEAL_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played: 
                    global potion_count 
                    if potion_count > 0:
                        ppl.get_health(100)
                        ppl.heal_self(can_heal=True)     
                        potion_count -= 1              
                    for btn in btns:
                        if btn != button2:
                            btn.is_locked = False 


                if PAPPER_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played:
                    move_list.clear()
                    move_list.append(button2)                     
                    for btn in btns:
                        game_obj.set_player_movement(f"{button2.text}", False)
                        if btn != button2:
                            btn.is_locked = False 

                if SCISSORS_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played:
                    move_list.clear() 
                    move_list.append(button3)                     
                    for btn in btns:
                        game_obj.set_player_movement(f"{button3.text}", False)
                        if btn != button3:
                            btn.is_locked = False 

                # if Player clicks on lock button for the first time. Save the selected move from above and tell the game that the player chose a move 
                if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and game_obj.temporary_move and (game_obj.player_played == False):
                    game_obj.set_player_movement(game_obj.temporary_move[0], True) # Call game function and save players move for the round 
                    game_obj.get_enemy_move(en_bot.set_bot_move(), enemy_played=True) # Call enemy_bot and ask it for a random move 
                    game_obj.lock_buttons() 

                # If Player has a locked move and clicks then say "You chose a move "
                if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and (game_obj.player_played == True):
                    button4.is_locked = True  

                # If Player has a locked move and clicks then say "You chose a move "
                if LOCK_BUTTON.checkForInput(MENU_MOUSE_POS) and (game_obj.player_played == False):
                    button4.is_locked = False  

                if END_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    run = False
                    sys.exit()

                if game_obj.both_played():
                    outcome = game_obj.winner_who(game_obj.player_move[0], game_obj.enemy_move[0])
                    if outcome == game_obj.player_name:
                        ppl.get_energy(100) 
                        game_obj.pla_att_anim()
                        moving_sprites.remove(ppl, een) 
                        moving_sprites.add(een, ppl)  
                        ppl.start_running() # Start the animation for attack 
                        print("You won")
                    elif outcome == game_obj.enemy_name:
                        een.get_energy(100)
                        game_obj.pla_att_anim()
                        moving_sprites.remove(een, ppl) 
                        moving_sprites.add(ppl, een)  
                        een.start_running() # Start the animation for attack 
                        print("Enemy won")
                    else:
                        print("Tie!")
                        game_obj.reset_buttons() 
                    game_obj.reset_moves()
                     

        if move_list and een.attack_done == True:
            game_obj.reset_buttons() 
            move_list.clear()
            for btn in btns:
                btn.is_locked = False 

        if move_list and ppl.attack_done == True:
            game_obj.reset_buttons() 
            move_list.clear() 
            for btn in btns:
                btn.is_locked = False 

        if game_obj.attack_anim and ppl.rect.center[0] >= 880:
            print("Colided with enemy")				
            een.health -= 12 
            een.get_damage(120)
            game_obj.sto_att_anim() 

        if game_obj.attack_anim and een.rect.center[0] <= 240:
            print("Colided with player")							
            ppl.health -= 12
            ppl.get_damage(120)
            game_obj.sto_att_anim()
        
        if een.health <= 0: 
            game_obj.game_obj.reset_buttons() 
            start_loading_screen()
            return False
        
        if ppl.health <= 0:
            game_obj.game_obj.reset_buttons() 
            start_loading_screen()
            return False

        SCREEN.blit(fps(), (550, 700))

        # Keep update in the end so there are no speed gliches 
        ppl.update()
        een.update()
        pygame.display.flip()
        pygame.display.update()

