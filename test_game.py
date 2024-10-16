from Player import Player
import random
random.seed(10)

def test_player():
    p = Player("TestPlayer")

    assert p.name == "TestPlayer"
    assert p.score == 0

    p.add_score(10)
    assert p.get_score() == 10

    p.add_score(5)
    assert p.get_score() == 15

    print(p)

import pytest
from Board import Board

def test_board():
    with pytest.raises(ValueError, match='Board size cant be less than 2'):
        b = Board(1,5)

    with pytest.raises(ValueError, match='Ship number must be greater than 0'):
        b = Board(10, 0)

    with pytest.raises(ValueError, match='Ship length cant be greater than board size'):
        b = Board(2, 3)
    b = Board(15, 5)

def test_coordinate():
    b = Board(10, 4)
    assert b.get_coordinate('abc') == -1
    assert b.get_coordinate(-2) == -1
    assert b.get_coordinate(11) == -1
    assert b.get_coordinate(1) == 1

def test_pick():
    b = Board(10, 4)
    print(b)
    assert b.pick(0,0) == 0
    assert b.pick(9,8) == 3
    assert b.pick(9, 8) == 0

def test_print():
    b = Board(5, 2)
    print(b)

def test_practice_game():
    b = Board(5,2)
    print(b)
    p = Player('One')
    assert p.name == 'One'
    assert p.score == 0
    assert b.size == 5
    assert b.ships == 2
    row = b.get_coordinate(3)
    assert row == 3
    column = b.get_coordinate(4)
    assert column == 4
    shot = b.pick(row,column)
    assert shot == 2
    assert b.pick(row, column) == 0
    p.add_score(shot)
    assert p.score == 2

@pytest.mark.parametrize('execution_number', range(5))
def test_game(execution_number):
    b = Board(10,10)