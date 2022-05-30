import pygame, sys
from buttons import * 
from Enemy_Champions import * 
from loading_screen import * 

'''
The enemy selection screen allows players to see a table with all available champions and their powers.
From there players pick a champion that will represent them in the batlle. This File is basically the same as the champion selection.py but it is 
just created to  create players that will sit on the right of the screen. Normally sprites could be used in order to have only one file insteaad of two 
but since time is limited two separete files were created.  
'''
pygame.init()
SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Champion Selection")

class ChampionSelector:
    def __init__(self):
        self.selected_champion = []
        self.is_locked = False 
        

    def champion_selection(self, clicked_champion):
        self.selected_champion.clear()
        self.selected_champion.append(clicked_champion)
        return self.selected_champion[0]


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

white = (255, 255, 255)
posX = 10
posY = 680

BG_FONT = pygame.transform.scale(pygame.image.load("assets/selection_bg.jpg").convert(), (1400, 790))
BG = pygame.transform.scale(pygame.image.load("assets/character_selection.png").convert_alpha(), (1120, 710))
font = pygame.font.Font("assets/font.ttf", 35)
stats_font = pygame.font.Font("assets/font.ttf", 12)
champ_selector = ChampionSelector()

	
# Colour constants 
BACKGROUND_COLOR = '#0d0e2e'
LIGHT_GRAY = '#ff3300' 
GRAY = '#33cc33'

button1 = Button(' ',100, 100,(120, 110),3)
button2 = Button(' ',100, 100,(235, 110),3)
button3 = Button(' ',100, 100,(350, 110),3)
button4 = Button(' ',100, 100,(470, 110),3)
button5 = Button(' ',100, 100,(120, 240),3)
button6 = Button(' ',100, 100,(235, 240),3)
button7 = Button(' ',100, 100,(350, 240),3)
button8 = Button(' ',100, 100,(470, 240),3)
button9 = Button(' ',100, 100,(120, 370),3)
button10 = Button(' ',100, 100,(235, 370),3)
button11 = Button(' ',100, 100,(350, 370),3)


btns = [button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11]
shown_champion = [EnemyMeleeChampionOne] 

def enemy_selector():
    run = True 
    while run:
        SCREEN.blit(BG_FONT, (0, 0))
        SCREEN.blit(BG, (50, 10))
        
        show_info = shown_champion[0]()
        SCREEN.blit(pygame.transform.scale(pygame.image.load(f"assets/{show_info.name}.png").convert_alpha(), (120, 120)), (700, 280))
        info_name = font.render( str(f"{show_info.name}"), True, (255, 255, 255)) 
        info_element = stats_font.render( str(f"Element: {show_info.element}"), True, (255, 255, 255)) 
        infor_weakness = stats_font.render( str(f"Weakness: {show_info.weakness}"), True, (255, 255, 255)) 
        infor_strong_against = stats_font.render( str(f"Strong aginst: {show_info.strong_against}"), True, (255, 255, 255)) 

        # Blit on screen 
        SCREEN.blit(info_element, (860, 300)) 
        SCREEN.blit(infor_weakness, (860, 335)) 
        SCREEN.blit(infor_strong_against, (860, 360)) 
        SCREEN.blit(info_name, (700, 135)) 

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        # Draw the highlights of the buttons 
        for highlight in btns:
            highlight.draw() 

        # TODO: change png to jpg 
        DASH_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Dash.png").convert_alpha(), (90,90)), pos=(170, 160), 
                            text_input=" ", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        
        CASANDRA_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Casandra.png").convert_alpha(), (90,90)), pos=(285, 160), 
                            text_input=" ", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        
        IVES_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Ives.png").convert_alpha(), (90,90)), pos=(400, 160), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        NORWIN_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Norwin.png").convert_alpha(), (90,90)), pos=(520, 160), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        HASSARON_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Hassaron.png").convert_alpha(), (90,90)), pos=(170, 290), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        IRATHAS_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Irathas.png").convert_alpha(), (90,90)), pos=(285, 290), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        IRGOMIR_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Irgomir.png").convert_alpha(), (90,90)), pos=(400, 290), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        LAMBERT_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Lambert.png").convert_alpha(), (90,90)), pos=(520, 290), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        NIMBUS_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Nimbus.png").convert_alpha(), (90,90)), pos=(170, 420), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        NOBURO_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Noburo.png").convert_alpha(), (90,90)), pos=(285, 420), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        YAHIRO_BUTTON = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Yahiro.png").convert_alpha(), (90,90)), pos=(400, 420), 
                            text_input=" ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        PLAY_BUTTON = BaseButton(image=None, pos=(1000, 540),  
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = BaseButton(image=None, pos=(1000, 590), 
                            text_input="Quit", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, QUIT_BUTTON, DASH_BUTTON, CASANDRA_BUTTON, IVES_BUTTON, NORWIN_BUTTON,
        HASSARON_BUTTON, IRATHAS_BUTTON, IRGOMIR_BUTTON, LAMBERT_BUTTON, NIMBUS_BUTTON, NOBURO_BUTTON, YAHIRO_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DASH_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # On the parameter set the name of the cliced champions sublcass 
                    champ_selector.champion_selection(EnemyMeleeChampionOne)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionOne)
                    for btn in btns:
                        if btn != button1:
                            btn.is_locked = False 

                if CASANDRA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionTwo)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionTwo)
                    for btn in btns:
                        if btn != button2:
                            btn.is_locked = False 

                if IVES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionThree)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionThree)
                    for btn in btns:
                        if btn != button3:
                            btn.is_locked = False  
                    
                if NORWIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionFour)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionFour)
                    for btn in btns:
                        if btn != button4:
                            btn.is_locked = False 

                if HASSARON_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionFive)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionFive)
                    for btn in btns:
                        if btn != button5:
                            btn.is_locked = False 

                if IRATHAS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionSix)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionSix)
                    for btn in btns:
                        if btn != button6:
                            btn.is_locked = False 

                if IRGOMIR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionSeven)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionSeven)
                    for btn in btns:
                        if btn != button7:
                            btn.is_locked = False 

                if LAMBERT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionEight)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionEight)
                    for btn in btns:
                        if btn != button8:
                            btn.is_locked = False 

                if NIMBUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionNine)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionNine)
                    for btn in btns:
                        if btn != button9:
                            btn.is_locked = False 

                if NOBURO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionTen)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionTen)
                    for btn in btns:
                        if btn != button10:
                            btn.is_locked = False 

                if YAHIRO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    champ_selector.champion_selection(EnemyMeleeChampionEleven)
                    shown_champion.clear()
                    shown_champion.append(EnemyMeleeChampionEleven)
                    for btn in btns:
                        if btn != button11:
                            btn.is_locked = False 

                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS) and not champ_selector.selected_champion:
                    print("You must choose a champion to play!")
                
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS) and champ_selector.selected_champion:
                    for btn in btns:   # Use this for loop to make sure no champion is preselected when starting a new game. 
                        btn.is_locked = False 
                    start_loading_screen() 
                    run = False 
                    return champ_selector.selected_champion[0]
                
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit() 

        pygame.display.update() 
