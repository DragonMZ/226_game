import random


class Board:

    def __init__(self, size: int, ships: int) -> None:
        """
        initializes the board, board size cant be negative and ship size cant be bigger than the board
        :param size: grid size, ie a 10x10 board
        :param ships: how many battleships are placed on the board
        """
        try:
            self.size = size
            self.ships = ships
            if 2 > size:
                raise ValueError('Board size cant be less than 2')
            if 1 > ships:
                raise ValueError('Ship number must be greater than 0')
            if ships > size:
                raise ValueError('Ship length cant be greater than board size')
        except ValueError as details:
            raise ValueError(details) from details

        self.board = [['_' for k in range(self.size)] for k in range(self.size)]
        self.place_ships()

    def __str__(self) -> str:
        """
        returns the values of the board as a string
        :return:
        """
        string = ''
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                string += str(self.board[i][j])
            string += '\n'
        return string

    def place_ships(self) -> None:
        """
        picks a random row, column and orientation (left, right, up, down)
        places 1 spot for ship 1, 2 spots for ship 2 etc.
        sequential spots for the same value ship are along the same axis (using orientation)
        if it reaches the end of the board it wraps around to the other side
        larger ships overwrite smaller ones
        :return:
        """
        for i in range(1, self.ships + 1):
            count = 1
            direction = random.randrange(4)
            row = random.randrange(self.size)
            column = random.randrange(self.size)
            self.board[row][column] = i
            while count < i:
                match direction:
                    case 0:
                        row -= 1
                        if row < 0:
                            row = self.size - 1
                    case 1:
                        row += 1
                        if row > self.size - 1:
                            row = 0
                    case 2:
                        column -= 1
                        if column < 0:
                            column = self.size - 1
                    case 3:
                        column += 1
                        if column > self.size - 1:
                            column = 0
                self.board[row][column] = i
                count += 1

    def get_coordinate(self, dot: int) -> int:
        """
        gets the user input, error checks it
        if valid returns it, if invalid returns -1 as an error code
        :param dot: user input
        :return: int within board size or -1 if fail
        """
        try:
            dot += 0
        except TypeError:
            print('Not an integer')
            return -1
        try:
            if 0 > dot:
                raise ValueError ('Out of bounds')
            if dot > self.size - 1:
                raise ValueError ('Out of bounds')
        except ValueError as details:
            print(str(details))
            return -1
        else:
            return dot

    def pick(self, row: int, column: int) -> int:
        """
        if the chosen coordinate has a value thats not _
        it returns the number that was there and sets the spot to _
        otherwise returns 0
        :param row: user input an int for row
        :param column:  user input an int for column
        :return: int
        """
        value = self.board[row][column]
        if value != '_':
            self.board[row][column] = '_'
            return value
        else:
            return 0
