from Board import Board
from Player import Player
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
import struct

HOST = '0.0.0.0'
PORT = 12345

b = Board(10, 4)

p = Player('One')
"""
prints the player name and score, then the visual of the board
asks for a row and column number, if numbers less than 0, not an int or bigger than board size throws error
if successful checks that coordinate and adds to the score (blanks return a score of zero)
runs infinitely currently
"""
with socket(AF_INET, SOCK_STREAM) as sock:
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        print(p)
        print(b)
        (sc, _) = sock.accept()
        with sc:
            data = sc.recv(1)
            hexData = data.hex()
            row = b.get_coordinate((data[0] & 0b11110000) >> 4)
            column = b.get_coordinate(data[0] & 0b00001111)
            if (row or column) == -1:
                break
            client, _ = sc.getpeername()
            print('Attack received:', client, ' ', hexData, ' ', row, ' ', column)
            shot = b.pick(row,column)
            p.add_score(shot)
            sc.sendall(struct.pack('!HH', p.get_score(), 0))