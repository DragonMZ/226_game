from django.test import TestCase
from .models import Player
from .models import Tile

# Create your tests here.
class PlayerTestCase(TestCase):
    def test_create(self):
        self.client.post('/game/create/')

        #are two players created
        p = Player.objects.all()
        p_count = p.count()
        self.assertEqual(p_count, 2)

        #is player one created
        p = Player.objects.get(name='One')
        self.assertEqual(p.name, 'One')
        self.assertEqual(p.score, 0)

        #is player two created
        p = Player.objects.get(name='Two')
        self.assertEqual(p.name, 'Two')
        self.assertEqual(p.score, 0)

        #are 100 tiles made
        t_count = Tile.objects.count()
        self.assertEqual(t_count, 100)

        #are treasures placed
        t_treasures = Tile.objects.filter(value=1).count()
        self.assertEqual(t_treasures, 4)

    def test_pick(self):
        #can player One pick from every tile
        self.client.post(f'/game/create/')
        p = Player.objects.filter(name='One')
        for row in range (10):
            for col in range (10):
                self.client.post(f'/game/pick/{p[0].name}/{row}/{col}/')
        self.assertEqual(p[0].score, 4)

        #can player Two pick from every tile
        self.client.post(f'/game/create/')
        p = Player.objects.filter(name='Two')
        for row in range (10):
            for col in range (10):
                self.client.post(f'/game/pick/{p[0].name}/{row}/{col}/')
        self.assertEqual(p[0].score, 4)

        #can player One pick from the empty board
        p = Player.objects.filter(name='One')
        for row in range (10):
            for col in range (10):
                self.client.post(f'/game/pick/{p[0].name}/{row}/{col}/')
        self.assertEqual(p[0].score, 0)

    def test_fail_states(self):
        self.client.post(f'/game/create/')

        #failing on row being text
        response = self.client.post('/game/pick/One/one/1/')
        self.assertContains(response, "You must input numbers for the row and column")

        #failing on col being text
        response = self.client.post('/game/pick/One/1/three/')
        self.assertContains(response, "You must input numbers for the row and column")

        #failing on row being out of bounds
        response = self.client.post('/game/pick/One/10/1/')
        self.assertContains(response, "Row and Col must be 0-9")

        #failing on col being out of bounds
        response = self.client.post('/game/pick/One/1/10/')
        self.assertContains(response, "Row and Col must be 0-9")

        #failing on invalid name
        response = self.client.post('/game/pick/Three/1/1/')
        self.assertContains(response, "Enter a valid player name")