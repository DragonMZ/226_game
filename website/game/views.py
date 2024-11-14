from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from .models import Player, Tile
import random

BOARD_SIZE = 10
NUM_TREASURES = 4

"""Main page, just gets all the players and tiles and displays them"""
def index(request):
    players = Player.objects.all()
    tiles = Tile.objects.all()
    context = {'board': tiles, 'player_list': players}
    return render(request, 'game/index.html', context)

"""Creating the board, first clearing it then making the players
creates a grid of tiles then randomly places a number of treasures"""
def create(request):
    Tile.objects.all().delete()
    Player.objects.all().delete()

    Player.create_player(name='One').save()
    Player.create_player(name='Two').save()

    #builds the YxY grid
    for i in range (BOARD_SIZE):
        for j in range (BOARD_SIZE):
            Tile.create_tile(row=i, col=j).save()

    #picks the random spots for the treasures
    for i in range(NUM_TREASURES):
        row = random.randrange(BOARD_SIZE)
        col = random.randrange(BOARD_SIZE)

        tiles = Tile.objects.filter(row=row, col=col)
        if len(tiles) == 1:
            tile = tiles[0]
            tile.value = 1
            tile.save()

    return redirect(index)

"""lets the player select the board throw /pick/player_name/row/col and serves
appropriate error pages if any of those are wrong. Gets the picked player and tile
and adds to their score if the tile had a non zero value"""
@transaction.atomic
def pick(request, name, row, col):
    #checks if non-int values were entered
    try:
        row = int(row)
        col = int(col)
    except (ValueError, TypeError):
        error = {'error': 'You must input numbers for the row and column'}
        return render(request, 'game/error.html', error)
    # checks for out of bounds
    if row < 0 or row > BOARD_SIZE-1 or col < 0 or col > BOARD_SIZE-1:
        error = {'error': 'Row and Col must be 0-9'}
        return render(request, 'game/error.html', error)

    tiles = Tile.objects.select_for_update().filter(row=row, col=col)
    players = Player.objects.select_for_update().filter(name=name)

    #checks if a valid player name was picked
    if len(players) == 1:
        player = players[0]
    else:
        error = {'error':'Enter a valid player name'}
        return render(request, 'game/error.html', error)

    if len(tiles) == 1:
        tile = tiles[0]
        if tile.value != 0:
            player.score += tile.value
            player.save()
            tile.value = 0
            tile.save()
        return redirect(index)

    #this shouldn't ever trigger but just in case it somehow finds no tiles at a row/col
    else:
        error = {'error':'No tile found'}
        return render(request, 'game/error.html', error)