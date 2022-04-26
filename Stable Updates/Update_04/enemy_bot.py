'''
This is a very simple EnemyBot that is used for every offline match with the player. 
Although simple it can be expanded so it becomes smarter and more responsive to users input (chat)
An AI can be created if time permits it. 
'''
import random
import time 

class Enemy: 
    def __init__(self):
        names = ["Mark", "John", "Steven", "Roger", "Joseph", "JOJO"]
        self.name = random.choice(names)
        self.can_move = True 
        self.bot_move = []

    def set_bot_move(self):
        moves = ["Rock", "Paper", "Scissors"]
        if self.can_move == True:
            moves = ["Rock", "Paper", "Scissors"]
            self.bot_move.append(random.choice(moves))
            return self.bot_move
        else:
            return str("You cant move yet")

    def clean_list(self):
        for i in self.bot_move[:]:
            if i != self.bot_move[0]:
                self.bot_move.remove(i)

    def bot_chater(self):
        phrases = ["HEllooo", "Whats up", "I will win", "This game is fun!"]
        return str(random.choice(phrases))

    def bot_color(self):
        colours = ["orange", "pink", "red", "green", "black"]
        return str(random.choice(colours))

