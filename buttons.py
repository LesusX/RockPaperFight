'''
In this file can be found all buttons used in the game.
Some are more advanced than the others but still functional and easy to use just by calling the class. 
'''
import pygame 
import sys 

# Main button used in the game. 
# This button can hold pictures, highlightet text and it is easilly positioned 
class BaseButton():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.is_locked = False 

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if not self.is_locked:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
        else:
            pass 

class SimpleButton:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 120
        self.height = 85
        self.is_locked = False 
        
    def button_state(self):
        return self.is_locked

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        if not self.is_locked:
            x1 = pos[0]
            y1 = pos[1]
            if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
                return True
            else:
                return False    
        else:
            print("Can't click now!")


# This is the highlighted part of the button 
# TODO Change the old name from Button to highlight or merge the two classes 
class Button:
    def __init__(self,text,width,height,pos,elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.is_locked = False 
        self.text = text

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#2E49A1'


    def draw(self):
        # elevation logic. Used more properly when the highlighted class connects with the Button class  
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation

        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_locked:
            self.top_color = '#D74B4B'
        if self.is_locked == False and self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.is_locked = True
        elif not self.is_locked and not self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#2E49A1'


# TODO: Remove the line below so that the window does not glitch 
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)
