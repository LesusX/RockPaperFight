import pygame 
screen = pygame.display.set_mode((1200,720))

class Champion(pygame.sprite.Sprite):
	def __init__(self, name, element, sprite_width, sprite_height, weakness, strong_against, arena_bonus):
		#-----------------------  Animation parameters -----------------------------------
		self.ultimate_attack_animation = False 
		self.ult_attack_animation = False
		self.run_right_animation = False 
		self.run_left_animation = False 
		self.attack_animation = False
		self.death_animation = False 
		self.idle_animation = False
		self.take_hit_right = False 
		self.hit_animation = False 
		self.death_right = False 
		self.ul_attack = False  		
		self.neg_vel = -15 
		self.vel = 15
		#----------------------------------------------------------
		self.name = name 
		self.element = element
		self.weakness = weakness 
		self.strong_against = strong_against 
		self.sprite_width = sprite_width
		self.sprite_height = sprite_height 
		self.arena_bonus = arena_bonus 
		#---------------------
		self.attack_damage = 100
		self.attack = False 
		self.heal = False 
		self.power_up = False
		self.attack_done = False 
		self.attack_landed = False 
		# Healthbar parameters 
		self.current_health = 1000
		self.target_health = 1000 
		self.max_health = 1000
		self.health_bar_length = 300
		self.health_ratio = self.max_health / self.health_bar_length
		self.health_change_speed = 5
		# Energybar parameters 
		self.energy = 100 # This is the reall amount of energy that each player starts with  
		self.current_energy = 100	# This is the amount of energy shown in the energy bar.
		self.target_energy = 100 
		self.max_energy = 1000
		self.energy_bar_length = 300
		self.energy_ratio = self.max_energy / self.energy_bar_length
		self.energy_change_speed = 5
#-------------------------- Animation functions -------------------------------
	def start_running(self):
		self.idle_animation = False 
		self.run_right_animation = True

	def start_idle(self):
		self.idle_animation = True

	def start_running_with_ult(self):
		self.ul_attack = True 
		self.idle_animation = False 
		self.run_right_animation = True

	def start_hit_anim(self):
		self.idle_animation = False 
		self.hit_animation = True 

	def start_death_animation(self):
		self.idle_animation = False 
		self.death_animation = True

	def reset_attack(self):
		self.attack_done = False 

	def reset_attack_landed(self):
		self.attack_landed = False 
	
	def reset_vel(self):
		self.vel = 15 

	def reset_neg_vel(self):
		self.neg_vel = -15

	#------------------ Energy and attack functions --------------------------------------
	def get_energy(self,amount):
		if self.target_energy < self.max_energy:
			self.target_energy += amount
			self.energy += amount  
		if self.target_energy > self.max_energy:
			self.target_energy = self.max_energy
			self.energy = self.max_energy
			
	def lose_energy(self,amount):
		if self.target_energy > 0:
			self.target_energy -= amount
		if self.target_energy < 0:
			self.target_energy = 0

	def reseT_energy(self):
		self.energy = 100
		self.target_energy = 100 

	def advanced_energy(self):
		transition_width = 0
		transition_color = (255, 222, 0)

		if self.current_energy < self.target_energy:
			self.current_energy += self.energy_change_speed
			transition_width = int((self.target_energy - self.current_energy) / self.energy_ratio)
			transition_color = (0,255,0)

		if self.current_energy > self.target_energy:
			self.current_energy -= self.energy_change_speed 
			transition_width = int((self.target_energy - self.current_energy) / self.energy_ratio)
			transition_color = (255,255,0)

		energy_bar_width = int(self.current_energy / self.energy_ratio)
		energy_bar = pygame.Rect(800,100,energy_bar_width,25)
		transition_bar = pygame.Rect(energy_bar.right,100,transition_width,25)
		
		pygame.draw.rect(screen,(255, 222, 0),energy_bar)
		pygame.draw.rect(screen,transition_color,transition_bar)	
		pygame.draw.rect(screen,(255,255,255),(800,100,self.energy_bar_length,25),4)	


	def get_damage(self,amount):
		if self.target_health > 0:
			self.target_health -= amount
		if self.target_health < 0:
			self.target_health = 0

	def get_health(self,amount):
		if self.target_health < self.max_health:
			self.target_health += amount
			self.health += amount
		if self.target_health > self.max_health:
			self.target_health = self.max_health
			self.health = self.max_health

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
		health_bar = pygame.Rect(800,70,health_bar_width,25)
		transition_bar = pygame.Rect(health_bar.right,100,transition_width,25)
		
		pygame.draw.rect(screen,(255,0,0),health_bar)
		pygame.draw.rect(screen,transition_color,transition_bar)	
		pygame.draw.rect(screen,(255,255,255),(800,70,self.health_bar_length,25),4)	


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

# Dash 
class EnemyMeleeChampionOne(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Dash", "Fire", 830, 550, "Dark", "Fire", "Desert")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Dash/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/idle_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Dash/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)),pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/attack_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Dash/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/take_hit_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/take_hit_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/take_hit_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Dash/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Dash/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/death_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/death_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/death_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Dash/death_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Dash/death_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height))]
		
		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),		
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_17.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Dash/ult_right_18.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [950, 200] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 

		if self.attack_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.45 
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]


		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Casandra
class EnemyMeleeChampionTwo(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Casandra", "Water", 1150, 700, "Air", "Fire", "Ice")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/idle_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)),pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/attack_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),		
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_17.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_18.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_19.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_20.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_21.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_22.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_23.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_24.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_25.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_26.png").convert_alpha(), (self.sprite_width, self.sprite_height)),		
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_27.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_28.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_29.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_30.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_31.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Casandra/ult_right_32.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Casandra/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/take_hit_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/take_hit_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/take_hit_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/take_hit_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)),pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)),pygame.transform.scale(pygame.image.load("champions/Casandra/death_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 120] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.45 
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Ives 
class EnemyMeleeChampionThree(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Ives", "Air", 1150, 650, "Fire", "Water", "Desert")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Ives/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Ives/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Ives/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Ives/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/idle_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),		
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_17.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_18.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_19.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_20.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_21.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_22.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_23.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_24.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_25.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_26.png").convert_alpha(), (self.sprite_width, self.sprite_height)),		
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_27.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_28.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_29.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Ives/ult_right_30.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Ives/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/take_hit_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Ives/take_hit_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/take_hit_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Ives/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_17.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Ives/death_right_18.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Ives/death_right_19.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 150] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.2
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]

		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.45 
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Norwin 
class EnemyMeleeChampionFour(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Norwin", "Air", 1090, 600, "Fire", "Water", "Desert")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/idle_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Norwin/ult_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Norwin/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/take_hit_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Norwin/take_hit_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/take_hit_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Norwin/death_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 170] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.2
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.45 
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Hassaron 
class EnemyMeleeChampionFive(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Hassaron", "Dark", 800, 850, "Fire", "Water", "Cave")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/idle_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Hassaron/ult_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Hassaron/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Hassaron/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Hassaron/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Hassaron/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Hassaron/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 320] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 

		
		if self.attack_animation:
			self.current_sprite += 0.2
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.45 
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Irathas 
class EnemyMeleeChampionSix(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Irathas", "Dark", 440, 500, "Fire", "Air", "Cave")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Irathas/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irathas/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irathas/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irathas/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/idle_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irathas/attack_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irathas/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/take_hit_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irathas/take_hit_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_17.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_18.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_19.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_20.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_21.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_22.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irathas/death_right_23.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 320] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.45
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.4
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Irgomir 
class EnemyMeleeChampionSeven(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Irgomir", "Air", 420, 350, "Fire", "Water", "Forest")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irgomir/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irgomir/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Irgomir/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irgomir/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Irgomir/death_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 325] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.4
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Lambert
class EnemyMeleeChampionEight(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Lambert", "Dark", 520, 450, "Fire", "Air", "Ice")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Lambert/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Lambert/idle_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/idle_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Lambert/ult_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Lambert/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/take_hit_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Lambert/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Lambert/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Lambert/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Lambert/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 350] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.4
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Nimbus 
class EnemyMeleeChampionNine(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Nimbus", "Dark", 310, 280, "Fire", "Air", "Cave")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Nimbus/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Nimbus/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Nimbus/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Nimbus/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Nimbus/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Nimbus/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_18.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_19.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_9.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_10.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_11.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_12.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_13.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_14.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_15.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_16.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_18.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Nimbus/attack_right_19.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Nimbus/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Nimbus/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Nimbus/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Nimbus/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 340] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.4
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.25 
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Noburo
class EnemyMeleeChampionTen(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Noburo", "Air", 840, 720, "Fire", "Water", "Forest")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Noburo/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Noburo/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Noburo/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Noburo/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Noburo/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Noburo/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Noburo/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Noburo/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Noburo/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Noburo/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Noburo/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Noburo/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Noburo/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Noburo/death_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 360] # Position of player 
		self.moving = pygame.Rect(180,355,400,450)

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 

		if self.attack_animation:
			self.current_sprite += 0.18
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.4
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.25 
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]

# Yahiro 
class EnemyMeleeChampionEleven(Champion, pygame.sprite.Sprite):
	def __init__(self):
		Champion.__init__(self, "Yahiro", "Dark", 850, 770, "Fire", "Water", "Cave")
		pygame.sprite.Sprite.__init__(self) 

		self.run_left_sprites = [pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_left_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.run_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_7.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/run_right_8.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.idle_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Yahiro/idle_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/idle_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Yahiro/idle_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/idle_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))] 

		self.attack_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Yahiro/attack_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Yahiro/attack_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Yahiro/attack_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Yahiro/attack_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Yahiro/attack_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Yahiro/attack_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.ult_right_sprites = [pygame.transform.scale(pygame.image.load("Champions/Yahiro/ult_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Yahiro/ult_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Yahiro/ult_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Yahiro/ult_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("Champions/Yahiro/ult_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("Champions/Yahiro/ult_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.take_hit_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Yahiro/take_hit_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/take_hit_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Yahiro/take_hit_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/take_hit_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height))]

		self.death_right_sprites = [pygame.transform.scale(pygame.image.load("champions/Yahiro/death_right_1.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/death_right_2.png").convert_alpha(), (self.sprite_width, self.sprite_height)),
		pygame.transform.scale(pygame.image.load("champions/Yahiro/death_right_3.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/death_right_4.png").convert_alpha(), (self.sprite_width, self.sprite_height)), 
		pygame.transform.scale(pygame.image.load("champions/Yahiro/death_right_5.png").convert_alpha(), (self.sprite_width, self.sprite_height)), pygame.transform.scale(pygame.image.load("champions/Yahiro/death_right_6.png").convert_alpha(), (self.sprite_width, self.sprite_height))]


		self.current_sprite = 0
		self.image = self.run_left_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.center = [980, 375] # Position of player 
		self.moving = pygame.Rect(180,355,400,450) 

	def update(self):
		self.advanced_health()
		self.advanced_energy()
		self.reset_attack()
		self.reset_attack_landed()

		if self.run_right_animation:	
			self.reset_neg_vel()
			self.rect.move_ip (self.neg_vel, 0) # Move the rectangle that holds the sprites by positive velocity so it moves left on x axis. 
			self.current_sprite += 0.45 
			if int(self.current_sprite) >= len(self.run_right_sprites):
				self.current_sprite = 0
			if self.rect.center[0] <= 285 and not self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.attack_animation = True 
			if self.rect.center[0] <= 300 and self.ul_attack:
				self.vel = 0 
				self.run_right_animation = False 
				self.ultimate_attack_animation = True 
			self.image = self.run_right_sprites[int(self.current_sprite)]

		if self.ultimate_attack_animation:
			self.attack_damage += 15
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.ult_right_sprites):
				self.current_sprite = 0
				self.ultimate_attack_animation = False 
				self.run_left_animation = True    
				self.attack_landed = True 
				self.ul_attack = False 
				self.attack_damage -= 15 
				self.reseT_energy()
			self.image = self.ult_right_sprites[int(self.current_sprite)] 


		if self.attack_animation:
			self.current_sprite += 0.3
			if int(self.current_sprite) >= len(self.attack_right_sprites):
				self.current_sprite = 0
				self.attack_animation = False 
				self.run_left_animation = True   
				self.attack_landed = True  
			self.image = self.attack_right_sprites[int(self.current_sprite)]


		if self.run_left_animation:
			self.reset_vel()
			self.current_sprite += 0.4
			self.rect.move_ip (self.vel, 0) # Move the rectangle that holds the sprites by negative velocity so it moves right on x axis.
			if int(self.current_sprite) >= len(self.run_left_sprites):
				self.current_sprite = 0
			if self.rect.center[0] >= 950:
				self.neg_vel = 0 
				self.run_left_animation = False
				self.attack_done = True 
				self.start_idle()
			self.image = self.run_left_sprites[int(self.current_sprite)]	

		if self.hit_animation:
			self.current_sprite += 0.15
			if int(self.current_sprite) >= len(self.take_hit_right_sprites):
				self.current_sprite = 0
				self.hit_animation = False 
				self.idle_animation = True    
			self.image = self.take_hit_right_sprites[int(self.current_sprite)]

		if self.death_animation:
			self.current_sprite += 0.25
			if int(self.current_sprite) >= len(self.death_right_sprites):
				self.current_sprite = 0
				self.death_animation = False 
			self.image = self.death_right_sprites[int(self.current_sprite)]

		if self.idle_animation:
			self.current_sprite += 0.25 
			if int(self.current_sprite) >= len(self.idle_right_sprites):
				self.current_sprite = 0

			self.image = self.idle_right_sprites[int(self.current_sprite)]


