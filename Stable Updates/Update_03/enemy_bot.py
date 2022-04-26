'''
This is a very simple EnemyBot that is used for every offline match with the player. 
Although simple it can be expanded so it becomes smarter and more responsive to users input (chat)
An AI can be created if time permits it. 
'''
import random 


class Enemy: 
    def __init__(self):
        names = ["Mark", "John", "Steven", "Roger", "Joseph", "JOJO"]
        self.name = random.choice(names)
        self.can_move = True 

    def bot_move(self):
        if self.can_move == True:
            moves = ["Rock", "Paper", "Scissors"]
            return str(random.choice(moves))
        else:
            return str("You cant move yet")

    def bot_chater(self):
        phrases = ["HEllooo", "Whats up", "I will win", "This game is fun!"]
        return str(random.choice(phrases))


x = Enemy()
'''
print(x.name)
x.can_move = False 
print(x.bot_move())
x.can_move = True  
print(x.bot_move())
'''










