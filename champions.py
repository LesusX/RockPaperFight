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

class MeleeChampionOne(Champion):
    def __init__(self):
        super().__init__()
        self.name = "Marcus Aurelius" 
        self.information = "Info about: Marcus Aurelius"
        self.type = "water"
        self.color = "black"

class MeleeChampionTwo(Champion):
    def __init__(self):
        super().__init__()
        self.name = "Julius Caesar" 
        self.information = "Info about: Julius Caesar"
        self.type = "Fire"
        self.color = "blue"

class RangeChampionOne(Champion):
    def __init__(self):
        super().__init__()
        self.name = "Septimius Severus" 
        self.information = "Info about: Septimius Severus"
        self.type = "Air"
        self.color = "orange"

