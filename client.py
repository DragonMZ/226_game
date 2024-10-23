from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)
from struct import pack, unpack

HOST = '127.0.0.1'
PORT = 12345


"""
TCP client, connects to hosts, waits to receive a name, if nothing received it terminates.
After getting the name prompts the user for a row and column as a single digit hex value
error checks, combines the two values into a single byte and sends it to the server
waits to receive the score from the server, which arrives as 2 unsigned shorts
The second should always be zero unless there is an error, then prints out your score
infinite loops currently
"""
with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    data = sock.recv(2)
    if len(data) == 0: #if received no data from server terminate, assuming its because too many concurrent users
        print("Too many connections")
        quit()
    name_len = unpack('!H', data)
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
            print('Value is greater than F')
            continue
        user_val = (user_row << 4 | user_col).to_bytes() #combines row and col
        sock.sendall(pack('!c', user_val)) #sends the combined value as a 1 byte char
        score = unpack('!HH',sock.recv(4)) #receives score from the server
        if score[1] != 0: # received out of bounds error, prompting a new row&col
            print('Selection out of bounds')
            continue
        print(name,"'s Score: ", score[0])