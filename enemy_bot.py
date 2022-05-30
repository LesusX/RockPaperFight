'''
This is a very simple EnemyBot that is used for every offline match with the player. 
Although simple it can be expanded so it becomes smarter and more responsive to users input (chat)
An AI can be created if time permits it. 
'''
import random

from Enemy_Champions import * 

class Enemy:  
    def __init__(self):
        names = ["Mark", "John", "Steven", "Roger", "Joseph", "JOJO"]
        self.name = random.choice(names)
        self.bot_move = []
        self.enemy_champion = []

    # Pick a random sublcass that represents a champion and return it to the offline_game.py to create an object 
    def pick_champion(self): 
        champions = [EnemyMeleeChampionOne, EnemyMeleeChampionTwo, EnemyMeleeChampionThree, EnemyMeleeChampionFour, EnemyMeleeChampionFive,
        EnemyMeleeChampionSix, EnemyMeleeChampionSeven, EnemyMeleeChampionEight, EnemyMeleeChampionNine, EnemyMeleeChampionTen, EnemyMeleeChampionEleven]
        self.enemy_champion.clear()
        self.enemy_champion.append(random.choice(champions))
        return self.enemy_champion[0]

    def set_bot_move(self): # There should be only three choices. Right now if the list has only 3 choices then it gives the same result 4> in a row- 
        moves = ["Rock", "Paper", "Scissors", "Rock", "Paper", "Scissors", "Paper", "Scissors"] # TODO: Fix the random choice so it does not give the same result more than 2 times in a row. 
        self.bot_move.clear() # Always clear the list before making a new choice 
        self.bot_move.append(random.choice(moves))
        return self.bot_move[0]

    # LEt the bot "talk" to the player. 
    def bot_chater(self):   # TODO Use these function on later versions of the game 
        phrases = ["HEllooo", "Whats up", "I will win", "This game is fun!"]
        return str(random.choice(phrases))
    # Set a color for the Bots avatar 
    def bot_color(self):
        colours = ["orange", "pink", "red", "green", "black"]
        return str(random.choice(colours))
