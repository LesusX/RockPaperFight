import socket
from _thread import *
import pickle
from game import Game
                    
'''
The server is the brain of the online game. Here information are collected from multiple clients. 
For every two active clients a game is created. 
'''
server = "SET_IPv4_HERE"  
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) 
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

moves = ["Rock", "Paper", "Scissors", "rock", "paper", "scissors", "ROCK", "PAPER", "SCISSORS"]

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))


    reply = ""
    while True:
        try:
            data = conn.recv(4096*6).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if p == 0:  # Get the data after the register word. The data should be the champions class name on a string form 
                        if data.split(" ")[0] == "register":
                            split_data = data.split(" ")
                            split_data.pop(0) 
                            x = ''.join(str(v) for v in split_data) # Connect all words to form properlly the name of the class 
                            game.set_champions(p, x)

                    if p == 1: 
                        if data.split(" ")[0] == "register":
                            split_data = data.split(" ")
                            split_data.pop(0) 
                            x = ''.join(str(v) for v in split_data) # Ensure that all parts of the object name are 
                            game.set_champions(p, x)
                    # Reset all play moves and as a result the game 
                    if data == "reset": 
                        game.resetWent()
                    # Register the move of each player 
                    if data != "get" and data in moves:
                        game.play(p, data)   

                    # Send to the clients data about the state of each players animation 
                    if data == "pla_att_anim":
                        game.pla_att_anim()
                    if data == "sto_att_anim":
                        game.sto_att_anim() 

                    if data == "reset_buttons":
                        game.reset_buttons() 


                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close() 

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    # For every connection of two create a new room/ game 
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId)) 
    
