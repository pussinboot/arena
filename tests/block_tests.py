import arena
import unittest
from config import token
from arena.blocks import Block

arena.access_token = token


class TestBlocks(unittest.TestCase):
    def setUp(self):
        self.block = Block('896296')

    def test_data(self):
        self.assertEqual(self.block.title, 'WELCOME TO THE BURRITO GALAXY WEBZONE')
        self.assertEqual(self.block.source['url'], 'http://burritogalaxy.com/')
