from Board import Board
from Player import Player
b = Board(10, 4)

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
    while True:
        row = b.get_coordinate(input('input row '))
        if row == -1:
            continue
        break
    while True:
        column = b.get_coordinate(input('input column '))
        if column == -1:
            continue
        break
    shot = b.pick(row,column)
    p.add_score(shot)