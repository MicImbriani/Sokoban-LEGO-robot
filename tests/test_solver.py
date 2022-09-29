import unittest

from sokoban.map_parser import MapParser
from sokoban.solver import Solver


class TestMap01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # Gets executed before all of the tests
        parser = MapParser()
        cls.map = parser.parse("../maps/map_01_one_can.txt")
        cls.solver = Solver(cls.map)

    def test_is_goal_state(self):
        cans = [1, 2, 3]
        goals = [1, 2, 3]
        self.assertTrue(self.solver.is_goal_state(cans, goals), "All cans on goals")

        cans = [1, 2, 4]
        goals = [1, 2, 3]
        self.assertFalse(self.solver.is_goal_state(cans, goals), "All cans not on goals")

    def test_get_actions(self):
        self.assertEqual([-1, -1, -1, -1], self.solver.get_actions(1, [31]), "Tile 1 actions")
        self.assertEqual([-1, 20, -1, 12], self.solver.get_actions(11, [31]), "Tile 11 actions")
        self.assertEqual([-1, 26, 16, -1], self.solver.get_actions(17, [31]), "Tile 17 actions")
        self.assertEqual([-1, -1, 29, 31], self.solver.get_actions(30, [31]), "Tile 30 actions (push free can)")
        self.assertEqual([-1, -1, 67, 69], self.solver.get_actions(68, [31]), "Tile 68 actions (step on goal)")


class TestMap03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # Gets executed before all of the tests
        parser = MapParser()
        cls.map = parser.parse("../maps/map_03_robot_on_goal.txt")
        cls.solver = Solver(cls.map)

    def test_get_actions(self):
        self.assertEqual([-1, 33, -1, -1], self.solver.get_actions(24, [15, 31, 53, 65]), "Tile 24 actions (blocked can on top)")
        self.assertEqual([-1, -1, 31, 33], self.solver.get_actions(32, [15, 31, 53, 65]), "Tile 32 actions (free can on the left)")
        self.assertEqual([-1, -1, 51, -1], self.solver.get_actions(52, [15, 31, 53, 65]), "Tile 52 actions (blocked can on the right)")
        self.assertEqual([-1, -1, -1, 67], self.solver.get_actions(66, [15, 31, 53, 65]), "Tile 6 actions (blocked can on the left)")

    def test_update_can_tile_ids(self):
        # Can moved up
        new_can_positions = self.solver.update_can_tile_ids([None, 29, 20], 20)
        self.assertEqual([11], new_can_positions, "Can moved from tile 20 to 11")

        # Can moved down
        new_can_positions = self.solver.update_can_tile_ids([None, 13, 22], 22)
        self.assertEqual([31], new_can_positions, "Can moved from tile 22 to 31")

        # Can moved left
        new_can_positions = self.solver.update_can_tile_ids([None, 14, 20, 13, 40], 13)
        self.assertEqual([20, 12, 40], new_can_positions, "Can moved from tile 13 to 12")

        # Can moved right
        new_can_positions = self.solver.update_can_tile_ids([None, 1, 2], 2)
        self.assertEqual([3], new_can_positions, "Can moved from tile 2 to 3")

class TestMap04(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = MapParser()
        cls.map = parser.parse("../maps/map_04_push_through_test.txt")
        cls.solver = Solver(cls.map)

    def test_push_through(self):
        self.assertEqual([-1, 22, 12, -1], self.solver.get_actions(13, [14, 15]), "Tile 13 (blocked on the right)")
        self.assertEqual([-1, -1, -1, 17], self.solver.get_actions(16, [14, 15]), "Tile 16 (blocked on the right)")


if __name__ == "__main__":
    unittest.main()
