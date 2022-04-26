'''
The game file is responsible for the logic of the game in both offline and online mode.
For the online mode the game needs a connection with the network file. 
'''
import random 

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


class OfflineGame: 
    def __init__(self):
        self.is_locked = False 
        self.player_played = False
        self.enemy_played = False 
        self.player_move = []
        self.enemy_move = []
        self.moves = [None, None]
        self.player_name = [] 
        self.enemy_name = []
        self.temporary_move = []
        self.winner = " "

    def get_enemy_move(self, enemy_played=False):
        self.enemy_played = enemy_played
        moves = ["Rock", "Paper", "Scissors"]
        if self.enemy_played:
            self.enemy_move.clear()
            self.enemy_move.append(random.choice(moves))       
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

    def winner_who(self, pl, en):
        if (pl == "Rock" and en == "Scissors") or (pl == "Paper" and en == "Rock") or (pl == "Scissors" and en == "Paper"):
            return str("WIN")
            # return str(f"WIN! You picked {pl}. Bot picked {en}")
        elif (pl == "Paper" and en == "Scissors") or (pl == "Rock" and en == "Paper") or (pl == "Scissors" and en == "Rock"):
            return str("DEFEAT")
            # return str(f"DEFEAT! You picked {pl}. Bot picked {en}")
        else:
            return str(f"TIE")

    def lock_timer(self, is_locked=False):
        self.is_locked = is_locked
        if self.is_locked:
            self.is_locked = True  
        elif not self.is_locked:
            self.is_locked = False 
            
    def reset_moves(self):
        self.player_played = False
        self.enemy_played = False 
