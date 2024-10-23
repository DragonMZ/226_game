from Board import Board
from Player import Player
from struct import pack, unpack
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
    SO_REUSEPORT
)
from threading import Semaphore, Thread, active_count


HOST = '0.0.0.0'
PORT = 12345
CONNECTIONS = 2 #maximum number of players
lock = Semaphore()
PLAYER_NAMES = ["One", "Two", "Three", "Four"] #array of player names to send out

b = Board(10, 4)

"""
Selects a user name from a list (active_count is default 1 and then goes up per thread, so it has to minus 2 to get
back to the start of the name array), encodes it and first sends the length of the name, and then the name
instantiates the new player and then begins the gameplay loop
waits for a 1 byte character to represent the row and column, left 4 bytes are the row, and then the column
if the value is out of bounds it will send an error code in two unsigned shorts, as the client is expecting its score.
the second short is always zero unless there is an error.
after getting valid coordinate it locks until it has converted the board value and added to score then after releasing
it will send the score off. reprints the board and player who just shot afterwards
"""
def handle_player(c_socket) -> None:
    with c_socket:
        name = PLAYER_NAMES[active_count() - 2]
        data = name.encode('utf-8')  # Convert command line arg to binary
        c_socket.sendall(pack('!H', len(data)))  # send length of the incoming name
        c_socket.sendall(data)  # send the name
        p = Player(name)
        while True:
            data = c_socket.recv(1)
            row = b.get_coordinate((data[0] & 0b11110000) >> 4)
            column = b.get_coordinate(data[0] & 0b00001111)
            if (row or column) == -1:
                c_socket.sendall(pack('!HH', 0, 1)) #if out of bounds sends error code
                continue
            client, _ = c_socket.getpeername()
            print('Attack received:', client, ' ', row, ' ', column)
            lock.acquire()
            shot = b.pick(row,column)
            lock.release()
            p.add_score(shot)
            c_socket.sendall(pack('!HH', p.get_score(), 0))
            print(b)
            print(p)

"""
Starts a server, when it gets a connection, if there is less than the number of users
it will start a new thread. So multiple people are shooting the same board.
"""
def start_server() -> None:
    s_sock = socket(AF_INET, SOCK_STREAM)
    s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 1)
    s_sock.bind((HOST, PORT))
    s_sock.listen(CONNECTIONS)
    while True:
        (sc, _) = s_sock.accept()
        t = Thread(target=handle_player, args=(sc,))
        if active_count() <= CONNECTIONS:
            t.start()
        else:
            print("Connection Refused")
            sc.close()


print(b)
start_server()