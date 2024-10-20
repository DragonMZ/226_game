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
CONNECTIONS = 2
lock = Semaphore()
PLAYER_NAMES = ["One", "Two", "Three", "Four"]

b = Board(10, 4)

def handle_player(c_socket):
    with c_socket:
        name = PLAYER_NAMES[active_count() - 2]
        data = name.encode('utf-8')  # Convert command line arg to binary
        c_socket.sendall(pack('!H', len(data)))  # send length of the incoming name
        c_socket.sendall(data)  # send the name
        p = Player(name)
        print(p)
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
            p.add_score(shot)
            lock.release()
            c_socket.sendall(pack('!HH', p.get_score(), 0))
            print(b)


def start_server():
    s_sock = socket(AF_INET, SOCK_STREAM)
    s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 1)
    s_sock.bind((HOST, PORT))
    s_sock.listen(CONNECTIONS)
    while True:
        (sc, _) = s_sock.accept()
        t = Thread(target=handle_player, args=(sc,))
        if active_count() <= CONNECTIONS:
            t.start()
            print(active_count())
        else:
            print("Too many connections")
            sc.close()

if '__main__' == __name__:
    print(b)
    start_server()