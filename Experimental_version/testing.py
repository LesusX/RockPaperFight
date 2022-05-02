from re import X
import pygame, sys

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, end):
		super().__init__()
		self.attack_sprites = [pygame.transform.scale(pygame.image.load("attack_1.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_2.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("attack_3.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_4.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_5.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_6.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_7.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_8.png").convert_alpha(), (300,330))]
		self.idle_sprites = [pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330)),]
		
		self.go_back = False 		
		self.attack_animation = False
		self.idle_animation = False
		self.current_sprite = 0
		self.image = self.attack_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
	
		self.x = x
		self.y = y 
		self.path = [x, end]
		self.vel = 7

	def update(self, attack=False, idle=False):
		self.move()

		self.attack_animation = attack
		if self.attack_animation:
			if self.x >= 20:
				self.current_sprite += 0.15
				self.rect.x += self.vel 
			if int(self.current_sprite) >= len(self.attack_sprites):
				self.current_sprite = 0
			self.idle_animation == True  
			self.image = self.attack_sprites[int(self.current_sprite)]
			
		'''
		self.go_back = back
		if self.go_back:
			if self.rect.x >= 20:
				self.current_sprite += 0.15
				self.rect.x -= self.vel 
			if self.rect.x <= 20:
				self.vel == 0 
			if int(self.current_sprite) >= len(self.attack_sprites):
				self.current_sprite = 0
				self.go_back = False
			self.idle_animation == False  
			self.image = self.attack_sprites[int(self.current_sprite)]
			# self.rect.x -= 10 
		'''

		self.idle_animation = idle
		if self.idle_animation:
			self.current_sprite += 0.10
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0
				self.idle_animation = False

			self.image = self.idle_sprites[int(self.current_sprite)]

	def move(self):
		if self.vel > 0:
			if self.x < self.path[1] + self.vel:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.x += self.vel
		else:
			if self.x > self.path[0] - self.vel:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.x += self.vel
				self.current_sprite = 0	

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 1200
screen_height = 750
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprite Animation")

POS_X = 200 
POS_Y = 500

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player(POS_X, POS_Y, 700)
moving_sprites.add(player)


BG = pygame.transform.scale(pygame.image.load("assets/pixel_forest.png").convert_alpha(), (1200, 720))


while True:
	player.update(attack=True, idle=False)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()



	# player.update(True, False)

	# Drawing
	screen.blit(BG, (0, 0))
	moving_sprites.draw(screen)
	pygame.display.flip()
	clock.tick(60)
	