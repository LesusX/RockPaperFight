import pygame
screen = pygame.display.set_mode((1200,720))

class Champion:
	def __init__(self):
		self.max_health = 100 
		self.health = 100 
		self.attack_damage = 10
		self.attack = False 
		self.heal = False 
		self.power_up = False 
		# Healthbar parameters 
		self.current_health = 1000
		self.target_health = 1000 
		self.max_health = 1000
		self.health_bar_length = 300
		self.health_ratio = self.max_health / self.health_bar_length
		self.health_change_speed = 5

	def get_damage(self,amount):
		if self.target_health > 0:
			self.target_health -= amount
		if self.target_health < 0:
			self.target_health = 0

	def get_health(self,amount):
		if self.target_health < self.max_health:
			self.target_health += amount
		if self.target_health > self.max_health:
			self.target_health = self.max_health

	def advanced_health(self):
		transition_width = 0
		transition_color = (255,0,0)

		if self.current_health < self.target_health:
			self.current_health += self.health_change_speed
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (0,255,0)

		if self.current_health > self.target_health:
			self.current_health -= self.health_change_speed 
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (255,255,0)

		health_bar_width = int(self.current_health / self.health_ratio)
		health_bar = pygame.Rect(200,70,health_bar_width,25)
		transition_bar = pygame.Rect(health_bar.right,45,transition_width,25)
		
		pygame.draw.rect(screen,(255,0,0),health_bar)
		pygame.draw.rect(screen,transition_color,transition_bar)
		pygame.draw.rect(screen,(255,255,255),(200,70,self.health_bar_length,25),4)

	def __str__(self) :
		return self.name

	def champion_power_up(self):
		self.attack_damage += 5

	def recieve_damage(self, damage_taken):
		self.health -= damage_taken
		return damage_taken

	def get_stamina(self):
		return self.stamina 

	# In the begining of the game apply a bonus from the arena to the champion. 
	# If the arena is not favorable to the champion lower damage and HP 
	def bonus_damage(self, arena_bonus_hp, arena_bonus_damage):
		if arena_bonus_damage and arena_bonus_hp >= 0: 
			self.health += arena_bonus_hp
			self.attack_damage += arena_bonus_damage
			return self.health, self.attack_damage
		elif arena_bonus_damage and arena_bonus_hp <= 0:
			self.health -= arena_bonus_hp
			self.attack_damage -= arena_bonus_damage            
			return self.health, self.attack_damage

	# The heal function lets the champion gain 10HP if it is allowed. 
	# In future version of the game stuns may block healing. 
	def heal_self(self, can_heal=False):
		self.heal = can_heal
		if self.heal and self.health <= (self.max_health - 10):
			self.heal += 10 
		elif self.heal and self.health > (self.max_health - 10):
			return str(f"You can't heal now. Health: {self.health}")

	def champion_information(self):
		return (f"\n{self.name} is clicked! \n{self.information}")


class MeleeChampionOne(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.name = "Marcus Aurelius" 
		self.information = "Info about: Marcus Aurelius"
		self.type = "water"
		self.color = "black"
		self.sprite_width = 600
		self.sprite_height = 660 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_sprites = [pygame.transform.scale(pygame.image.load("champions/blue_knight/idle_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/idle_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/blue_knight/idle_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/idle_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/blue_knight/idle_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/idle_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/blue_knight/idle_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/blue_knight/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.attack_left_sprites = [pygame.transform.scale(pygame.image.load("Champions/blue_knight/attack_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/blue_knight/attack_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/blue_knight/attack_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/blue_knight/attack_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/blue_knight/attack_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/blue_knight/attack_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/blue_knight/attack_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_animation = False 
		self.run_left_animation = False 
		self.attack_animation = False
		self.idle_animation = False
		self.current_sprite = 0
		self.image = self.attack_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [180,355] # Fixed position of player 

		self.vel = 6
		self.neg_vel = -7 

	def start_running(self):
		self.idle_animation = False 
		self.run_left_animation = True

	def start_idle(self):
		self.idle_animation = True

	def reset_vel(self):
		self.vel = 6 
	
	def reset_neg_vel(self):
		self.neg_vel = -7  

	def update(self):
		self.advanced_health()

		if self.run_left_animation:
			self.reset_vel()
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.2 
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 880:
				self.vel = 0 
				self.run_left_animation = False 
				self.attack_animation = True    
			self.image = self.run_left_sprites[int(self.current_sprite)]

		if self.attack_animation:
			self.current_sprite += 0.088 
			if int(self.current_sprite) >= len(self.attack_left_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_right_animation = True    
			self.image = self.attack_left_sprites[int(self.current_sprite)]

		if self.run_right_animation:
			self.reset_neg_vel()
			self.current_sprite += 0.2 
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 180:
				self.neg_vel = 0 
				self.run_right_animation = False
				self.start_idle()
			self.image = self.run_right_sprites[int(self.current_sprite)]	

		if self.idle_animation:
			self.current_sprite += 0.10
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0

			self.image = self.idle_sprites[int(self.current_sprite)]


class MeleeChampionTwo(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.name = "Julius Caesar" 
		self.information = "Info about: Julius Caesar"
		self.type = "Fire"
		self.color = "blue"


		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_left_1.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_left_2.png").convert_alpha(), (250,260 )),
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_left_3.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_left_4.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_left_5.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_left_6.png").convert_alpha(), (250,260 ))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_right_1.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("champions/blue_warrior/run_right_2.png").convert_alpha(), (250,260 )),
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_right_3.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_right_4.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_right_5.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/run_right_6.png").convert_alpha(), (250,260 ))] 

		self.idle_sprites = [pygame.transform.scale(pygame.image.load("Champions/blue_warrior/idle_left_1.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/idle_left_2.png").convert_alpha(), (250,260 )),
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/idle_left_3.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/idle_left_4.png").convert_alpha(), (250,260 ))]

		self.attack_left_sprites = [pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_1.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_2.png").convert_alpha(), (250,260 )),
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_3.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_4.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_5.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_6.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_7.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_8.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("champions/blue_warrior/attack_left_4.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_9.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_10.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_11.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_12.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("champions/blue_warrior/attack_left_4.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_13.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_14.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_15.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_16.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("champions/blue_warrior/attack_left_4.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_17.png").convert_alpha(), (250,260 )), pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_18.png").convert_alpha(), (250,260 )), 
		pygame.transform.scale(pygame.image.load("Champions/blue_warrior/attack_left_19.png").convert_alpha(), (250,260 ))]


		self.run_right_animation = False 
		self.run_left_animation = False
		self.attack_animation = False
		self.idle_animation = False
		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [180,330] # Fixed position of player 

		self.vel = 6
		self.neg_vel = -7 

	def start_running(self):
		self.idle_animation = False 
		self.run_left_animation = True

	def start_idle(self):
		self.idle_animation = True

	def reset_vel(self):
		self.vel = 6 
	
	def reset_neg_vel(self):
		self.neg_vel = -7 

	def update(self):
		self.advanced_health()

		if self.run_left_animation:
			self.reset_vel()
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.2 
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 880:
				self.vel = 0 
				self.run_left_animation = False 
				self.attack_animation = True    
			self.image = self.run_left_sprites[int(self.current_sprite)]

		if self.attack_animation:
			self.current_sprite += 0.15 
			if int(self.current_sprite) >= len(self.attack_left_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_right_animation = True    
			self.image = self.attack_left_sprites[int(self.current_sprite)]

		if self.run_right_animation:
			self.reset_neg_vel()
			self.current_sprite += 0.2 
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 180:
				self.neg_vel = 0 
				self.run_right_animation = False
				self.start_idle()
			self.image = self.run_right_sprites[int(self.current_sprite)]	

		if self.idle_animation:
			self.current_sprite += 0.10
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0

			self.image = self.idle_sprites[int(self.current_sprite)]



class MeleeChampionThree(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.name = "Caesar Augustus " 
		self.information = "Info about: Marcus Aurelius"
		self.type = "water"
		self.color = "black"
		self.sprite_width = 370 
		self.sprite_height = 430


		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_sprites = [pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/idle_left_9.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/purple_warrior/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.attack_left_sprites = [pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/purple_warrior/attack_left_12.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_animation = False 
		self.run_left_animation = False 
		self.attack_animation = False
		self.idle_animation = False
		self.current_sprite = 0
		self.image = self.attack_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [180,325] # Fixed position of player 

		self.vel = 6
		self.neg_vel = -7 

	def start_running(self):
		self.idle_animation = False 
		self.run_left_animation = True

	def start_idle(self):
		self.idle_animation = True

	def reset_vel(self):
		self.vel = 7 
	
	def reset_neg_vel(self):
		self.neg_vel = -7  

	def update(self):
		self.advanced_health()

		if self.run_left_animation:
			self.reset_vel()
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.2 
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 880:
				self.vel = 0 
				self.run_left_animation = False 
				self.attack_animation = True    
			self.image = self.run_left_sprites[int(self.current_sprite)]

		if self.attack_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.attack_left_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_right_animation = True    
			self.image = self.attack_left_sprites[int(self.current_sprite)]

		if self.run_right_animation:
			self.reset_neg_vel()
			self.current_sprite += 0.2 
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 180:
				self.neg_vel = 0 
				self.run_right_animation = False
				self.start_idle()
			self.image = self.run_right_sprites[int(self.current_sprite)]	

		if self.idle_animation:
			self.current_sprite += 0.2
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0

			self.image = self.idle_sprites[int(self.current_sprite)]


class RangeChampionOne(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.name = "Septimius Severus" 
		self.information = "Info about: Septimius Severus"
		self.type = "Air"
		self.color = "orange"
		self.sprite_width = 300 
		self.sprite_height = 360

		self.idle_sprites = [pygame.transform.scale(pygame.image.load("Champions/green_archer/idle_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/green_archer/idle_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.attack_left_sprites = [pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),  
		pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/green_archer/attack_left_13.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.attack_animation = False
		self.idle_animation = False
		self.current_sprite = 0
		self.image = self.attack_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [180,330] # Fixed position of player 

		self.vel = 6
		self.neg_vel = -7 
		

	def start_running(self):
		self.idle_animation = False 
		self.attack_animation = True 

	def start_idle(self):
		self.idle_animation = True


	def update(self):
		self.advanced_health()

		if self.attack_animation:
			self.current_sprite += 0.2 
			if int(self.current_sprite) >= len(self.attack_left_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.start_idle()
			self.image = self.attack_left_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.10
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0

			self.image = self.idle_sprites[int(self.current_sprite)]
