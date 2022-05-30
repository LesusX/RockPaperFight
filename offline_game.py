'''
Here is the offline part of the program. 
While offline, players can play against randomly generated bots and even interact with them. 
'''
import random
from pkg_resources import safe_extra
import pygame, sys
from buttons import * 
from game import OfflineGame
import enemy_bot
from loading_screen import * 


# Basic for starting pygame properly 
pygame.init()
SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Menu")
font = pygame.font.Font("assets/font.ttf", 25)
stats_font = pygame.font.Font("assets/font.ttf", 14)
result_font = pygame.font.Font("assets/font.ttf", 40)
# Use PosX, posY to set the position of the chosen champions name 
posX = 5
posY = 700
arenas = ["forest", "ice", "cave", "desert"] 

move_list = [] # Store temporarly any move made. Based on the move here a button will be highlighted 

button1 = Button('Rock',130, 40, (265, 530),5)
button2 = Button('Paper',130, 40,(265, 580),5)
button3 = Button('Scissors',190, 40,(245, 630),5)
button4 = Button('Lock',200, 50,(480, 530),5)
button5 = Button('Heal',140, 30,(480, 600),5)

btns = [button1, button2, button3, button4, button5]
potion_count = 2
enemy_potion_count = 2 

game_paused = False    
energy_attack_ready = False 
enemy_energy_attack_ready = False 

pygame.mixer.init()

# Get the font that will be used for all text in the game 
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

'''
Use redraw_win to clean the main while loop on man_menu_x
'''
def redraw_win(SCREEN, BG, BOX, time, MENU_TEXT, MENU_RECT, moving_sprites, btns, game_buttons, MENU_MOUSE_POS, PAUSE_MENU, pause_menu_buttons):
    global game_paused

    if game_paused:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(BOX, (210, 480))

        for btn in btns:
            btn.draw()

        # Get a hold of all available buttons and render them 
        for button in game_buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        moving_sprites.draw(SCREEN)
        SCREEN.blit(PAUSE_MENU, (380, 100))
        
        for btnn in pause_menu_buttons:
            btnn.changeColor(MENU_MOUSE_POS)
            btnn.update(SCREEN)
        SCREEN.blit(time, (490, 100))        
    else:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(BOX, (210, 480))


        for btn in btns:
            btn.draw()

        # Get a hold of all available buttons and render them 
        for button in game_buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(time, (490, 100))
        moving_sprites.draw(SCREEN)

# Check if the player clicked the settings button 
def settigns_state(comand):
    global game_paused
    if comand == "active":
        game_paused = True 
    elif comand == "inactive":
        game_paused = False

def main_menu_x(pl):
    global clock
    global game_paused 
    global potion_count 
    global enemy_potion_count
    global energy_attack_ready 
    global enemy_energy_attack_ready
    # ------ Start the music only when the game is ready --------------------
    my_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')
    my_sound.play()
    music_volume = 0.1

    # Create the Enemy 
    en_bot = enemy_bot.Enemy()
    q = en_bot.pick_champion() 

    game_obj = OfflineGame()   
    # Champions objects 
    # Get the name of the selected champions subcless and create an object to be used on this game.
    # The positions of the characters are fixed in the champions file 
    moving_sprites = pygame.sprite.Group()
    champion_zero = pl() 
    champion_one = q()
    moving_sprites.add(champion_zero, champion_one) 

    # Time variables 
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks() # Let pygame count the ticks for time 
    minutes_played = 0 

    # ------ Add Bonus to champions -----------
    arena_type = random.choice(arenas) 

    if arena_type == champion_zero.element: 
        champion_zero.attack_damage += 3
    if arena_type == champion_one.element: 
        champion_one.attack_damage += 3
    # ----- Nerf champions based on the openent ---------------
    if champion_one.element == champion_zero.weakness:
        champion_zero.attack_damage -= 3
    if champion_zero.element == champion_one.weakness:
        champion_zero.attack_damage -= 3

    # Objects that will be shown on the screen 
    BG = pygame.transform.scale(pygame.image.load(f"assets/arenas/{arena_type}_arena.png").convert_alpha(), (1200, 720))
    PAUSE_MENU = pygame.transform.scale(pygame.image.load(f"assets/pause_menu.png").convert_alpha(), (380, 480))
    BOX = pygame.transform.scale(pygame.image.load("assets/input_box.jpg").convert_alpha(), (750, 210))
    MENU_TEXT = get_font(37).render(f"{champion_zero.name}    vs    {champion_one.name}", True, "#FF421A")
    MENU_RECT = MENU_TEXT.get_rect(center=(600, 50))


    # Start the idle before the loop so it doesn't block the updates 
    champion_zero.start_idle()
    champion_one.start_idle()
    while True:
        clock.tick(30)  
        # Get the seconds within the gaem and blit the on the screen 
        seconds = int((pygame.time.get_ticks()-start_ticks)/1000) #calculate how many seconds
        time = font.render("Time: " + str(f"{minutes_played}:{seconds}"), True, (255, 255, 255))

        # Every 60 seconds add 1 minute on the timer and restart the pygame timer to count again all seconds from 0-60 
        if seconds == 60:
            start_ticks = pygame.time.get_ticks()
            minutes_played += 1

        # Create the buttons 
        END_BUTTON = BaseButton(image=None, pos=(570, 250), 
                            text_input="Exit Program", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        QUIT_GAME_BUTTON = BaseButton(image=None, pos=(570, 460), 
                            text_input="Quit Game", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        UNPAUSE_BUTTON = BaseButton(image=None, pos=(570, 530), 
                            text_input="UNPAUSE", font=get_font(25), base_color="#11FF00", hovering_color="#BCFDB7")

        PAUSE_BUTTON = BaseButton(image=None, pos=(800, 580), 
                            text_input="PAUSE", font=get_font(25), base_color="#11FF00", hovering_color="#BCFDB7")

        ROCK_BUTTON = BaseButton(image=None, pos=(332, 540), 
                            text_input="Rock", font=get_font(25), base_color="#11FF00", hovering_color="#BCFDB7")

        PAPER_BUTTON = BaseButton(image=None, pos=(335, 590), 
                            text_input="Paper", font=get_font(25), base_color="#11FF00", hovering_color="#BCFDB7")

        SCISSORS_BUTTON = BaseButton(image=None, pos=(340, 640), 
                            text_input="Scissors", font=get_font(25), base_color="#11FF00", hovering_color="#BCFDB7")

        HEAL_BUTTON = BaseButton(image=None, pos=(555, 610), 
                            text_input="Heal", font=get_font(25), base_color="#11FF00", hovering_color="#BCFDB7")

        LOCK_BUTTON = BaseButton(image=None, pos=(578, 550), 
                            text_input="LOCK MOVE", font=get_font(20), base_color="#11FF00", hovering_color="#BCFDB7")

        VOLUME_UP_BUTTON = BaseButton(image=None, pos=(490, 390), 
                            text_input="Vol.UP", font=get_font(18), base_color="#11FF00", hovering_color="#BCFDB7")

        VOLUME_DOWN_BUTTON = BaseButton(image=None, pos=(660, 390), 
                            text_input="Vol.Down", font=get_font(18), base_color="#11FF00", hovering_color="#BCFDB7")


        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Hold all buttons together in two lists. One for the normal game buttons and one for the menu buttons 
        # Pause menu buttons should not be able to be clicked when they are not visible 
        pause_menu_buttons = [UNPAUSE_BUTTON, QUIT_GAME_BUTTON, END_BUTTON, VOLUME_UP_BUTTON, VOLUME_DOWN_BUTTON]
        game_buttons = [ROCK_BUTTON, PAPER_BUTTON, SCISSORS_BUTTON, LOCK_BUTTON, HEAL_BUTTON, PAUSE_BUTTON]

        # For better organisation place here things tha must be rendered on the screen 
        redraw_win(SCREEN, BG, BOX, time, MENU_TEXT, MENU_RECT, moving_sprites, btns, game_buttons, MENU_MOUSE_POS, PAUSE_MENU, pause_menu_buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game_obj.game_buttons_locked == False:
                if QUIT_GAME_BUTTON.checkForInput(MENU_MOUSE_POS) and game_paused:
                    game_obj.reset_buttons() 
                    start_loading_screen()
                    potion_count = 2 
                    game_paused = False 
                    my_sound.stop() 
                    return False 

                # Let the player heal if there are enough potions left 
                if HEAL_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played: 
                    if potion_count > 0:
                        champion_zero.get_health(100)
                        champion_zero.heal_self(can_heal=True)     
                        potion_count -= 1              
                    for btn in btns:
                        if btn != button2:
                            btn.is_locked = False

                # Let the player click the button and save the move of the button on a temporary list 
                # If later on the player clicks lock save the temporary move as permanent for the round  
                if ROCK_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played: 
                    move_list.clear() 
                    move_list.append(button1)                                             
                    for btn in btns:                                            # players movements and register´temporary move. 
                        game_obj.set_player_movement(f"{button1.text}", False)   # Call the game function responsible for the 
                        if btn != button1:                                       
                            btn.is_locked = False                                

                if PAPER_BUTTON.checkForInput(MENU_MOUSE_POS) and not game_obj.player_played:
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

                # ------------------- SETTINGS BUTTONS ---------------------------------------------------
                if PAUSE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ROCK_BUTTON.is_locked = True 
                    PAPER_BUTTON.is_locked = True 
                    SCISSORS_BUTTON = True 
                    LOCK_BUTTON.is_locked = True 
                    settigns_state("active")

                if VOLUME_UP_BUTTON.checkForInput(MENU_MOUSE_POS) and game_paused:
                    if music_volume < 1:
                        music_volume += 0.1
                        my_sound.set_volume(music_volume)

                if VOLUME_DOWN_BUTTON.checkForInput(MENU_MOUSE_POS) and game_paused:
                    if music_volume >= 0:
                        music_volume -= 0.1
                        my_sound.set_volume(music_volume)


                if UNPAUSE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ROCK_BUTTON.is_locked = False 
                    PAPER_BUTTON.is_locked = False  
                    SCISSORS_BUTTON = False  
                    LOCK_BUTTON.is_locked = False  
                    settigns_state("inactive")
                   
                
                if END_BUTTON.checkForInput(MENU_MOUSE_POS) and game_paused:
                    pygame.quit()
                    run = False
                    sys.exit()
                
                # ----------------------------  Animation Logic --------------------------------------
                if game_obj.both_played():
                    outcome = game_obj.winner_who(game_obj.player_move[0], game_obj.enemy_move[0])
                    if outcome == game_obj.player_name:
                        # Show who won the round and wait 2 seconds  
                        result = result_font.render( str(f"{champion_zero.name} won the round!"), True, (255, 0, 0)) 
                        SCREEN.blit(result, (120, 270))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        #  CDepending on the collected energy, start ult attack animation or a normal one  
                        if energy_attack_ready:
                            game_obj.pla_att_anim()
                            moving_sprites.empty()  
                            moving_sprites.add(champion_one, champion_zero)  
                            champion_zero.start_running_with_ult() # Start the animation for attack 
                        else:
                            champion_zero.get_energy(100) 
                            game_obj.pla_att_anim()
                            moving_sprites.empty() 
                            moving_sprites.add(champion_one, champion_zero)  
                            champion_zero.start_running() # Start the animation for attack
                    elif outcome == game_obj.enemy_name:
                        # Show who won the round and wait 2 seconds  
                        result = result_font.render( str(f"{champion_one.name} won the round!"), True, (255, 0, 0)) 
                        SCREEN.blit(result, (120, 270))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        if enemy_energy_attack_ready:
                            game_obj.pla_att_anim()
                            moving_sprites.empty()  
                            moving_sprites.add(champion_zero, champion_one)  
                            champion_one.start_running_with_ult() # Start the animation for attack 
                        else:
                            #  Depending on the collected energy, start ult attack animation or a normal one  
                            champion_one.get_energy(100)         
                            game_obj.pla_att_anim()
                            moving_sprites.empty()  
                            moving_sprites.add(champion_zero, champion_one)  
                            champion_one.start_running() # Start the animation for attack                     
                    else:
                        # Show who won the round and wait 2 seconds  
                        result = result_font.render( str("Tie! No one won!"), True, (255, 0, 0)) 
                        SCREEN.blit(result, (120, 270))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        game_obj.reset_buttons() 
                        for btn in btns: 
                            btn.is_locked = False 

                    game_obj.reset_moves()

        if champion_zero.energy >= 1000:
            energy_attack_ready = True 

        if champion_one.energy >= 1000:
            enemy_energy_attack_ready = True 


        if move_list and champion_one.attack_done == True:
            game_obj.reset_buttons() 
            move_list.clear()
            for btn in btns:
                btn.is_locked = False 

        if move_list and champion_zero.attack_done == True:
            game_obj.reset_buttons() 
            move_list.clear() 
            for btn in btns:
                btn.is_locked = False 

        if game_obj.attack_anim and champion_zero.rect.center[0] >= 790:
            champion_one.health -= 12 
            champion_one.get_damage(120)
            game_obj.sto_att_anim() 

        if game_obj.attack_anim and champion_one.rect.center[0] <= 280:
            champion_zero.health -= 12
            champion_zero.get_damage(120)
            game_obj.sto_att_anim()


        if game_obj.attack_anim and champion_one.rect.center[0] <= 330:
            champion_zero.start_hit_anim() 
            
        if game_obj.attack_anim and champion_zero.rect.center[0] >= 770:
            champion_one.start_hit_anim() 


        if champion_one.health <= 50 and enemy_potion_count > 0:
            champion_one.health += 10
            enemy_potion_count -= 1

        # Ending if enemy looses. Reset everything in the game
        if champion_one.health <= 0: 
            result = result_font.render( str(f"{champion_zero.name} won the round!"), True, (255, 0, 0)) 
            SCREEN.blit(result, (120, 270))
            pygame.display.update()
            pygame.time.delay(2000)
            my_sound.stop() 
            game_obj.reset_buttons() 
            start_loading_screen()
            potion_count = 2
            enemy_potion_count = 2
            game_paused = False 
            return False
        
        # Ending if player looses. Reset everything in the game
        if champion_zero.health <= 0:
            result = result_font.render( str(f"{champion_one.name} won the round!"), True, (255, 0, 0)) 
            SCREEN.blit(result, (120, 270))
            pygame.display.update()
            pygame.time.delay(2000)
            champion_zero.start_death_animation()  # TODO: Fix the death animation so that it show in the end of the game. 
            my_sound.stop()
            game_obj.reset_buttons() 
            start_loading_screen()
            potion_count = 2 
            enemy_potion_count = 2
            game_paused = False 
            return False

        # Keep update in the end so there are no speed gliches 
        champion_zero.update()
        champion_one.update()
        pygame.display.flip()

