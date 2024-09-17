import random

class Board:
    def __init__(self, size, ships):
        self.size = size
        self.ships = ships
        self.board = [['_' for k in range(self.size)] for k in range(self.size)]

    def place_ships(self):
        for i in range(1, self.ships + 1):
            count = 1
            direction = random.randrange(3)
            row = random.randrange(10)
            column = random.randrange(10)
            self.board[row][column] = i
            while count < i:
                match direction:
                    case 0:
                        row -= 1
                        if row < 0:
                            row = self.size - 1
                    case 1:
                        row += 1
                        if row > self.size:
                            row = 0
                    case 2:
                        column -= 1
                        if column < 0:
                            column = self.size - 1
                    case 3:
                        column += 1
                        if column > self.size:
                            column = 0
                self.board[row][column] = i
                count += 1

    def __str__(self):
        string = ''
        for j in range(len(self.board)):
            for i in range(len(self.board)):
                string += str(self.board[j][i])
            string += '\n'
        return string


b = Board(10, 4)
b.place_ships()
print(b)