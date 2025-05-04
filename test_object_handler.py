import unittest
import pygame
import math
from mapas import *
from unittest.mock import MagicMock
from constant import TILESIZE  # Assuming TILESIZE is defined in constant.py

class TestMap(unittest.TestCase):
    def setUp(self):
        pygame.init()  # Needed for surface creation
        self.screen = MagicMock()  # Mock screen for rendering tests
        self.map = Map()
        
    def test_position_within_wall(self):
        # Test positions that should hit walls (value 1)
        self.assertEqual(self.map.position(0, 0), 1)  # Top-left corner
        self.assertEqual(self.map.position(TILESIZE * 14, TILESIZE * 9), 1)  # Bottom-right corner
        self.assertEqual(self.map.position(TILESIZE * 2, TILESIZE * 5), 1)  # Middle wall
        
    def test_position_within_empty_space(self):
        # Test positions that should be empty (value 0)
        self.assertEqual(self.map.position(TILESIZE * 1, TILESIZE * 1), 0)  # First empty cell
        self.assertEqual(self.map.position(TILESIZE * 13, TILESIZE * 1), 0)  # Right-side empty
        
    def test_position_special_tile(self):
        # Test the special win tile (value 4)
        self.assertEqual(self.map.position(TILESIZE * 2, TILESIZE * 5), 4)
        
    def test_position_out_of_bounds(self):
        # Test handling of out-of-bounds coordinates
        with self.assertRaises(IndexError):
            self.map.position(TILESIZE * 15, TILESIZE * 5)  # X out of bounds
        with self.assertRaises(IndexError):
            self.map.position(TILESIZE * 5, TILESIZE * 10)  # Y out of bounds
            
    def test_render_wall_tiles(self):
        self.map.render(self.screen)
        # Verify wall tiles are drawn with black color
        call_args = [args[0] for args, _ in self.screen.fill.call_args_list]
        self.assertIn((0, 0, 0), call_args)
        
    def test_render_empty_tiles(self):
        self.map.render(self.screen)
        # Verify empty tiles are drawn with white color
        call_args = [args[0] for args, _ in self.screen.fill.call_args_list]
        self.assertIn((255, 255, 255), call_args)
        
    def test_win_condition_true(self):
        # Create a mock player facing the win tile (position (2,5))
        player = MagicMock()
        player._x = TILESIZE * 1  # One tile left of win tile
        player._y = TILESIZE * 5
        player._rotation_angle = 0  # Facing right
        
        self.assertTrue(self.map.win_condition(player))
        
    def test_win_condition_false(self):
        # Create a mock player not facing the win tile
        player = MagicMock()
        player._x = TILESIZE * 1
        player._y = TILESIZE * 1
        player._rotation_angle = math.pi  # Facing left
        
        self.assertFalse(self.map.win_condition(player))
        
    def test_win_condition_edge_case(self):
        # Test when player is exactly on the win tile
        player = MagicMock()
        player._x = TILESIZE * 2.5  # Center of win tile
        player._y = TILESIZE * 5.5
        player._rotation_angle = 0
        
        self.assertTrue(self.map.win_condition(player))

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()