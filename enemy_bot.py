'''
This is a very simple EnemyBot that is used for every offline match with the player. 
Although simple it can be expanded so it becomes smarter and more responsive to users input (chat)
An AI can be created if time permits it. 
'''
import random
from winreg import EnableReflectionKey

from champions import * 
class Enemy:  
    def __init__(self):
        names = ["Mark", "John", "Steven", "Roger", "Joseph", "JOJO"]
        self.name = random.choice(names)
        self.bot_move = []
        self.enemy_champion = []

    # Pick a random sublcass that represents a champion and return it to the offline_game.py to create an object 
    def pick_champion(self):
        champions = [MeleeChampionOne, MeleeChampionTwo, RangeChampionOne]
        self.enemy_champion.clear()
        self.enemy_champion.append(random.choice(champions))
        return self.enemy_champion[0]

    def set_bot_move(self):
        moves = ["Rock", "Paper", "Scissors"]
        self.bot_move.clear()
        self.bot_move.append(random.choice(moves))
        return self.bot_move[0]

    def bot_chater(self):
        phrases = ["HEllooo", "Whats up", "I will win", "This game is fun!"]
        return str(random.choice(phrases))

    def bot_color(self):
        colours = ["orange", "pink", "red", "green", "black"]
        return str(random.choice(colours))
