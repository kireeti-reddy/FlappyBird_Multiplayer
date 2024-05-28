import socket
from _thread import *
from player import Player
import pickle
import random

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

SCREENWIDTH = 611
SCREENHEIGHT = 511
players = [Player(50, 50, {}, {}, ''), Player(100, 100, {}, {}, '')]

GROUNDY = SCREENHEIGHT * 0.8
def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data


            if players[player].msg == "crashed":
                conn.sendall(pickle.dumps("Game Over"))
                break
            
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


def game_elements():
    
    #BACKGROUND = [GAME_SPRITES['background1'], GAME_SPRITES['background2'], GAME_SPRITES['background3']]
    #BASE = [GAME_SPRITES['base1'], GAME_SPRITES['base2'], GAME_SPRITES['base3']]
    #score = 0
    basex = 0
    #inv_velX = SCREENWIDTH/2
    #inv_velY = 0 
    #inv_score = random.randint(2,5)
    #invincible = False  # Initially, the player is not invincible
    #invincibility_duration = 20  # Duration of invincibility in seconds
    #invincibility_timer = 0  # Initialize invincibility timer
    #remaining_time = 0
    #bird2_velX = SCREENWIDTH +10
    #bird2_velY = (SCREENHEIGHT-112)/2
    #bird2_spawn = random.randint(7,12)
    #bird2_collide = False

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    #horizontal and vertical velocity
    
        

    return upperPipes, lowerPipes

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen

    The lower pipe is initially generated using which the upper pipe location is decided
    """
    pipeHeight = 320
    offset = SCREENHEIGHT/4 #decides the distance between the pipes
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - 112  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10 # the place where the pipes are generated
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

a = game_elements()
print("here")
players[0].upperpipes = a[0]
players[0].lowerpipes = a[1]
players[1].upperpipes = a[0]
players[1].lowerpipes = a[1]

    

connected_players = 0
currentPlayer = 0
# Modify the server loop to start the game only when all players are connected
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    connected_players += 1