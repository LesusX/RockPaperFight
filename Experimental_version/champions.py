import pygame 

class Champion:
	def __init__(self):
		self.max_health = 100 
		self.health = 100 
		self.attack_damage = 10
		self.attack = False 
		self.heal = False 
		self.power_up = False 

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
	def __init__(self, x, y):
		Champion.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.name = "Marcus Aurelius" 
		self.information = "Info about: Marcus Aurelius"
		self.type = "water"
		self.color = "black"

		self.attack_animation = False
		self.idle_animation = False
		self.attack_sprites = [pygame.transform.scale(pygame.image.load("attack_1.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_2.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("attack_3.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_4.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_5.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_6.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_7.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_8.png").convert_alpha(), (300,330))]
		
		self.idle_sprites = [pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330))]
		
		self.current_sprite = 0
		self.image = self.attack_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.topleft = [x, y]

	def attack(self):
		self.attack_animation = True

	def idle(self):
		self.idle_animation = True

	def update(self, attack=False, idle=False):
		self.attack_animation = attack
		self.idle_animation = idle 
		if self.attack_animation == True:
			self.rect.x += 8
			self.current_sprite += 0.2 
			if int(self.current_sprite) >= len(self.attack_sprites):
				self.current_sprite = 0
			if self.rect.x == 5:
				self.attack_animation = False 
				self.idle_animation = True 
			self.image = self.attack_sprites[int(self.current_sprite)]
		
		if self.idle_animation == True:
			self.current_sprite += 0.10
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0

			self.image = self.idle_sprites[int(self.current_sprite)]



class MeleeChampionTwo(Champion, pygame.sprite.Sprite):
	def __init__(self, x, y):
		Champion.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.name = "Julius Caesar" 
		self.information = "Info about: Julius Caesar"
		self.type = "Fire"
		self.color = "blue"

		self.attack_animation = False
		self.idle_animation = False
		self.attack_sprites = [pygame.transform.scale(pygame.image.load("attack_1.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_2.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("attack_3.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_4.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_5.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_6.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_7.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_8.png").convert_alpha(), (300,330))]
		
		self.idle_sprites = [pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330))]
		
		self.current_sprite = 0
		self.image = self.attack_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.topleft = [x, y]

	def attack(self):
		self.attack_animation = True

	def idle(self):
		self.idle_animation = True

	def update(self, attack=False, idle=False):
		self.attack_animation = attack
		self.idle_animation = idle 
		if self.attack_animation == True:
			self.rect.x += 8
			self.current_sprite += 0.2 
			if int(self.current_sprite) >= len(self.attack_sprites):
				self.current_sprite = 0
			if self.rect.x == 5:
				self.attack_animation = False 
				self.idle_animation = True 
			self.image = self.attack_sprites[int(self.current_sprite)]
		
		if self.idle_animation == True:
			self.current_sprite += 0.10
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0

			self.image = self.idle_sprites[int(self.current_sprite)]


class RangeChampionOne(Champion, pygame.sprite.Sprite):
	def __init__(self, x, y):
		Champion.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.name = "Septimius Severus" 
		self.information = "Info about: Septimius Severus"
		self.type = "Air"
		self.color = "orange"

		self.attack_animation = False
		self.idle_animation = False
		self.attack_sprites = [pygame.transform.scale(pygame.image.load("attack_1.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_2.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("attack_3.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_4.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_5.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_6.png").convert_alpha(), (300,330)), 
		pygame.transform.scale(pygame.image.load("attack_7.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("attack_8.png").convert_alpha(), (300,330))]
		
		self.idle_sprites = [pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_01.png").convert_alpha(), (300,330)),
		pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330)), pygame.transform.scale(pygame.image.load("idle_02.png").convert_alpha(), (300,330))]
		
		self.current_sprite = 0
		self.image = self.attack_sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.topleft = [x, y]

	def attack(self):
		self.attack_animation = True

	def idle(self):
		self.idle_animation = True

	def update(self, attack=False, idle=False):
		self.attack_animation = attack
		self.idle_animation = idle 
		if self.attack_animation == True:
			self.rect.x += 8
			self.current_sprite += 0.2 
			if int(self.current_sprite) >= len(self.attack_sprites):
				self.current_sprite = 0
			if self.rect.x == 5:
				self.attack_animation = False 
				self.idle_animation = True 
			self.image = self.attack_sprites[int(self.current_sprite)]
		
		if self.idle_animation == True:
			self.current_sprite += 0.10
			if int(self.current_sprite) >= len(self.idle_sprites):
				self.current_sprite = 0

			self.image = self.idle_sprites[int(self.current_sprite)]