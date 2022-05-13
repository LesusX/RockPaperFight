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


# With SchampoionSelector the game cotrols if a champion is chosen so it can be then send to the main game.
# If no champions are locked then the player can not click play.
#TODO: A function could replace this class. If there is time replace it. If there is no time fuck it. Let it be as it is. 
class ChampionSelector:
    def __init__(self):
        self.selected_champion = []
        self.is_locked = False 
        

    def champion_selection(self, clicked_champion):
        self.selected_champion.clear()
        self.selected_champion.append(clicked_champion)
        return self.selected_champion[0]



def show_champ(x,y, name):
    x_name = font.render("You:" + str(name), True, (255, 255, 255))
    SCREEN.blit(x_name, (x,y))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)



white = (255, 255, 255)
posX = 10
posY = 680

BG = pygame.transform.scale(pygame.image.load("assets/purple_background.png").convert(), (1400, 790))
font = pygame.font.Font("assets/font.ttf", 35)
sel = pygame.image.load("assets/selector.png").convert()
champ_selector = ChampionSelector()



def enemy_selector():
    run = True 
    name = " "  
    while run:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(sel, (150, 80))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("Select your champion", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(575, 40))

        CHAMPION_A = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/Caesar.png").convert_alpha(), (120,120)), pos=(270, 170), 
                            text_input=" ", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        CHAMPION_B = BaseButton(image=pygame.transform.scale(pygame.image.load("assets/aurelius.png").convert_alpha(), (120, 120)), pos=(500, 170), 
                            text_input=" ", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
            
        PLAY_BUTTON = BaseButton(image=None, pos=(1100, 630),  
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = BaseButton(image=None, pos=(1100, 680), 
                            text_input="Quit", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)


        for button in [PLAY_BUTTON, QUIT_BUTTON, CHAMPION_A, CHAMPION_B]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CHAMPION_A.checkForInput(MENU_MOUSE_POS):
                    # On the parameter set the name of the cliced champions sublcass 
                    champ_selector.champion_selection(EnemyMeleeChampionOne)

                if CHAMPION_B.checkForInput(MENU_MOUSE_POS):
                    # On the parameter set the name of the cliced champions sublcass 
                    champ_selector.champion_selection(EnemyMeleeChampionTwo)


                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS) and not champ_selector.selected_champion:
                    print("You must choose a champion to play!")
                
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS) and champ_selector.selected_champion:
                    start_loading_screen() 
                    run = False 
                    return champ_selector.selected_champion[0]
                
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit() 

        show_champ(posX,posY, name)       
        pygame.display.update() 
