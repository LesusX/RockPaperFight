import pygame
pygame.init()

win = pygame.display.set_mode((1200, 720))

pygame.display.set_caption("First Game")

bg = pygame.transform.scale(pygame.image.load("assets/pixel_forest.png").convert(), (1200, 720))
char = pygame.image.load('idle_01.png')

clock = pygame.time.Clock()


class enemy(object):
    walkRight = [pygame.transform.scale(pygame.image.load("attack_1.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_2.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("attack_3.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_4.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_5.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_6.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_7.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_8.png").convert_alpha(), (300,330))]
		
    walkLeft = [pygame.transform.scale(pygame.image.load("attack_1.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_2.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("attack_3.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_4.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_5.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_6.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_7.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_8.png").convert_alpha(), (300,330))]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 15

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 8:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3 ], (self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3 ], (self.x,self.y))
            self.walkCount += 1
            
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        


def redrawGameWindow():
    win.blit(bg, (0,0))
    goblin.draw(win)
    pygame.display.update()


#mainloop
goblin = enemy(100, 410, 64, 64, 500)
run = True
while run:
    
    clock.tick(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    redrawGameWindow()

pygame.quit()