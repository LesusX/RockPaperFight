'''
The game file is responsible for the logic of the game in both offline and online mode.
For the online mode the game needs a connection with the network file. 
'''

class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False



'''
Offline game handles the moves of the player and the enmy bot. 
At the same time it handles the show of basic inforamtion and the chat between Player and bot. 
'''
class OfflineGame: 
    def __init__(self, player_name, enemy_name):
        self.can_bot_talk = False
        self.player_name = player_name  
        self.player_played = False
        self.player_move = []
        self.enemy_name = enemy_name
        self.enemy_played = False 
        self.enemy_move = []
        self.temporary_move = []
        self.waiting = False  
        self.winner = [] 
        self.is_animation_playing = False 

    def get_enemy_move(self,enemy_input, enemy_played=False):
        self.enemy_played = enemy_played
        if self.enemy_played:
            self.enemy_move.clear()
            self.enemy_move.append(enemy_input)       
            self.enemy_played == True 
            
    def set_player_movement(self, TOF, player_played=False):
        self.player_played = player_played
        if self.player_played:
            self.player_move.clear()
            self.player_move.append(TOF)  
        elif not self.player_played:
            self.temporary_move.clear()
            self.temporary_move.append(TOF)

    def both_played(self):
        if self.player_played and self.enemy_played:
            return True 
        elif not self.player_played or not self.enemy_played:
            return False 

    def wait_for_enemy(self):
        self.waiting = True 
        return self.waiting 

    # Based on the input from both Player and Enemy find out who is the winner and return the result 
    def winner_who(self, pl, en):
        self.winner.clear() 
        if (pl == "Rock" and en == "Scissors") or (pl == "Paper" and en == "Rock") or (pl == "Scissors" and en == "Paper"):
            self.winner.append(pl) 
            return str(f"{self.player_name}")
            # return str("WIN")
        elif (pl == "Paper" and en == "Scissors") or (pl == "Rock" and en == "Paper") or (pl == "Scissors" and en == "Rock"):
            self.winner.append(en) 
            return str(f"{self.enemy_name}")
            # return str("DEFEAT")
        else:
            return str(f"TIE")

    # This function allows the enemy bot to speak based on the timer on the Offlne_game.py 
    def lock_timer(self, can_bot_talk=False):
        self.can_bot_talk = can_bot_talk
        if self.can_bot_talk:
            self.can_bot_talk = True  
        elif not self.can_bot_talk:
            self.can_bot_talk = False 

    # Reset the moves of both players so that the second round can start 
    def reset_moves(self):
        self.temporary_move.clear()
        self.player_played = False
        self.enemy_played = False 
