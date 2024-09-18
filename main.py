from Board import Board
from Player import Player
b = Board(10, 4)
b.place_ships()

p = Player('One')
"""
prints the player name and score, then the visual of the board
asks for a row and column number, if numbers less than 0, not an int or bigger than board size throws error
if successful checks that coordinate and adds to the score (blanks return a score of zero)
runs infinitely currently
"""
while True:
    print(p)
    print(b)
    try:
        row = int(input('input row ')) - 1
        if 0 > row:
            raise ValueError ('Out of bounds')
        if row > b.size - 1:
            raise ValueError ('Out of bounds')
    except ValueError as details:
        print(str(details))
        continue
    try:
        column = int(input('input column ')) - 1
        if 0 > column:
            raise ValueError ('Out of bounds')
        if column > b.size - 1:
            raise ValueError ('Out of bounds')
    except ValueError as details:
        print(str(details))
        continue
    shot = b.pick(row,column)
    p.add_score(shot)