from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from .models import Player, Tile
import random

BOARD_SIZE = 10
NUM_TREASURES = 4

def index(request):
    players = Player.objects.all()
    tiles = Tile.objects.all()
    context = {'board': tiles, 'player_list': players}
    return render(request, 'game/index.html', context)

def create(request):
    Tile.objects.all().delete()
    Player.objects.all().delete()
    Player.create_player(name='One').save()
    Player.create_player(name='Two').save()
    output = ''
    for i in range (BOARD_SIZE):
        for j in range (BOARD_SIZE):
            Tile.create_tile(row=i, col=j).save()
    for i in range(NUM_TREASURES):
        row = random.randrange(BOARD_SIZE)
        col = random.randrange(BOARD_SIZE)
        tiles = Tile.objects.filter(row=row, col=col)
        if len(tiles) == 1:
            tile = tiles[0]
            tile.value = 1
            tile.save()
            output += f'Added treasure {i}<br>'
        else:
            output += f"Couldn't add treasure {i}<br>"
    return redirect(index)

@transaction.atomic
def pick(request, name, row, col):
    try:
        row = int(row)
        col = int(col)
    except (ValueError, TypeError):
        error = {'error': 'You must input numbers for the row and column'}
        return render(request, 'game/error.html', error)
    if row < 0 or row > 9 or col < 0 or col > 9:
        error = {'error': 'Row and Col must be 0-9'}
        return render(request, 'game/error.html', error)

    tiles = Tile.objects.select_for_update().filter(row=row, col=col)
    players = Player.objects.select_for_update().filter(name=name)
    if len(players) == 1:
        player = players[0]
    else:
        error = {'error':'Enter a valid player name'}
        return render(request, 'game/error.html', error)
    if len(tiles) == 1:
        tile = tiles[0]
        if tile.value != 0:
            tile.value = 0
            tile.save()
            player.score += 1
            player.save()
        return redirect(index)
    else:
        error = {'error':'No tile found'}
        return render(request, 'game/error.html', error)