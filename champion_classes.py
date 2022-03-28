'''
The Champion class is a generic class that provides all basic properties found amongst all champions in the game. 
Some of the properties are health, damage calculation, recognition of the type of damage taken and defence mechanisms. 
'''

from multiprocessing import managers


class Champions:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = int(health)
        self.damage = int(damage)
        self.recieved_attack = []
        self.is_attacking = False   
        self.is_defending = False
        self.is_idle = False 

    def basic_defence(self):
        health = self.health
        health -= 10
        self.health = health
        return f"You lost 10 life points. \nHealth: {health}"

    def ultimate_attack(self):
        damage = self.damage
        damage += 20
        return damage 

    '''
    Based on the damage taken by enemy champions aply the proper amount of damage to the health bar. In case where there are aplied effects such as poison, stun etc. 
    damage is either increased or multiplied by x amount. 
    '''
    def calculate_damge_taken(self, attack):  # TODO Change the class so it registers the enemies element/type so it is easier to write the code
        if attack == "fire_ball":
            self.health -= 30
            print (f"You got damaged by an {attack} Your lifepoints have fallen to {self.health} now!") 
        elif attack == "ice_ball":
            self.health -= 25
            print (f"You got damaged by an {attack} Your lifepoints have fallen to {self.health} now!") 


'''
Monster class has more specific abilities that all monsters have. These abilities are quicker stamina regeneration, weaknesses and more. 
In case of having multiple monster types this will serve as a good template.
'''

class Monster(Champions):
    def __init__(self, name, health, damage, stamina):
        super().__init__(name, health, damage)
        self.stamina = stamina
        self.type = "beast"

    def __str__(self):
        return f"Name: {self.name} \nHealth: {self.health} \nStamina: {self.stamina} \nBase Damage: {self.damage} \nMonster type: {self.type}"



"""
Mage class has more specific abilities that all mages should have. These abilities are quicker mana regeneration, weaknesses and more. 
"""
class Mage(Champions):
    range_damage = 20

    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.mana = 100 

    def __str__(self):
        return f"Name: {self.name} \nHealth: {self.health} \nBase Damage: {self.damage}"

    def mana_regeneration(self):
        self.mana += 20 
        return f"Mana increased to {self.mana}" 



class FireMage(Mage):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.mage_type = "Fire Mage"
        self.element = "Fire"

    def __str__(self):
        return super().__str__() + f"\nType: {self.mage_type}"

    def fire_attack(self):
        damage = self.damage
        damage += 30
        return f"You dealt {damage} damage to your enemy"


class IceMage(Mage):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.mage_type = "Ice Mage"
        self.element = "Ice"
        
    def __str__(self):
        return super().__str__() + f"\nType: {self.mage_type}"

    def ice_attack(self):
        damage = self.damage
        damage += 20
        return f"You dealt {damage} damage to your enemy"
