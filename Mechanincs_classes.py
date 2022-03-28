from champion_classes import *

weakneses = {"champion_weknesses":{"ice_mage":{'weakness':'ice', 'favourable_battlefield': 'fire'}, "fire_mage":{'weakness':'ice', 'favorable_batlefield':'fire'} }    }


class BattleSystem:
    def __init__(self, first_champion, second_champion):
        self.first_champion = first_champion 
        self.second_champion = second_champion 

    def __str__(self) -> str:
        return f"{self.first_champion.mage_type} vs {self.second_champion.mage_type}"

    def calculate_damage(self):
        pass
        
    def calcuate_effects(self):
        pass

    def strongest_player(self): # TODO make tupell that defines advantages
        pass



# mage = IceMage("Mark", 100, 23)
# print(mage)
'''
first_champ = IceMage("Mark", 120, 23)
second_champ = FireMage("John", 100, 32)
x = BattleSystem(first_champ, second_champ)
print("------------------------------------------------\n")
print(x)
print("\n------------------------------------------------\n")
attack = input("Attack with a: ") 
first_champ.calculate_damge_taken(attack)
'''
