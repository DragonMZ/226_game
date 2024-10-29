from Board import Board
from Player import Player
from struct import pack
from asyncio import (
    run,
    start_server,
    StreamReader,
    StreamWriter,
)

HOST = '0.0.0.0'
PORT = 12345
ENCODING = 'utf-8'
CONNECTIONS = 2 #maximum number of players
PLAYER_NAMES = ["One", "Two", "Three", "Four"] #array of player names to send out
PLAYER = 0 #variable to track which player name to assign

b = Board(10, 4)

"""
Refuses further players after reaching the connection limit
Selects a user name from a list, encodes it and first sends the length of the name, and then the name
instantiates the new player and then begins the gameplay loop
waits for a 1 byte character to represent the row and column, left 4 bytes are the row, and then the column
if the value is out of bounds it will send an error code in same format as the score (second unsigned short is nonzero).
checks the coordinates and returns the updated score, score is sent as 2 unsigned shorts, second is always 0
"""
async def handle_player(reader: StreamReader, writer: StreamWriter) -> None:
    global PLAYER
    if PLAYER >= CONNECTIONS:
        print('Connection Refused')
        writer.close()
        await writer.wait_closed()
        return

    name = PLAYER_NAMES[PLAYER] # assign a player name
    PLAYER += 1
    data = name.encode(ENCODING)
    writer.write(pack('!H', len(data))) #send length of name
    await writer.drain()
    writer.write(data) #send name
    await writer.drain()
    p = Player(name)
    print(p)

    while True:
        data = await reader.readexactly(1) #wait to receive row/col data in 1 byte
        row = b.get_coordinate((data[0] & 0b11110000) >> 4) #only get the left 4 bits then bit shift received data to get row
        column = b.get_coordinate(data[0] & 0b00001111) #only get right 4 bits for col
        if (row or column) == -1:
            writer.write(pack('!HH', 0, 1)) #sends error value for invalid coordinates
            continue
        print('Attack received:', writer.get_extra_info('peername'), ' ', row, ' ', column)
        shot = b.pick(row, column)
        p.add_score(shot)
        writer.write(pack('!HH', p.get_score(), 0)) #sends score as two unsigned shorts
        print(b)

"""Starts the server"""
async def main():
    server = await start_server(handle_player, HOST, PORT)
    await server.serve_forever()

if '__main__' == __name__:
    print(b)
    run(main())