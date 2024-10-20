from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)
from sys import argv
from struct import pack, unpack

HOST = '127.0.0.1'
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    name_len = unpack('!H', sock.recv(2))
    name = sock.recv(name_len[0]).decode('utf-8')
    while True:
        try:
            print("Enter a Row in hex (0-F)")
            user_row = abs(int(input(), 16)) #gets user input as a hex value
            print("Enter a Column in hex (0-F)")
            user_col = abs(int(input(), 16))
        except ValueError:
            print('Invalid input')
            continue
        if user_row | user_col > 15: # throws away input if bigger than a hex value
            continue
        user_val = (user_row << 4 | user_col).to_bytes() #combines row and col
        sock.sendall(pack('!c', user_val)) #sends the combined value as a 1 byte char
        score = unpack('!HH',sock.recv(4)) #receives score from the server
        if score[1] == 1: # received out of bounds error, prompting a new row&col
            continue
        print(name,"'s Score: ", score[0])