import unittest


import sys
# setting path
sys.path.append('D:/Users/imbrm/GitHub/ITU/AdvancedRobotics')


from sokoban.map_parser import MapParser
from sokoban.solver import Solver



class TestMap01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # Gets executed before all of the tests
        cls.parser = MapParser()  # "cls.parser" is a class variable (shared across all instances)
        cls.map = cls.parser.parse("D:/Users/imbrm/GitHub/ITU/AdvancedRobotics/maps/map_01_one_can.txt")

    def test_goals(self):
        self.assertEqual([67], self.map.goals)

    def test_cans(self):
        self.assertEqual([31], self.map.cans)

    def test_robot(self):
        self.assertEqual([11], self.map.robot)

    def assert_wall(self, wall_to_assert, walls, wall_name):
        set_diff = wall_to_assert.difference(walls)
        self.assertTrue(len(set_diff) == 0, f"{wall_name} wall parsed\n\n{set_diff} not in\n{walls}")
        [walls.remove(wall) for wall in wall_to_assert]  # Remove wall

    def test_walls(self):
        walls = set(self.map.walls)
        top_wall = set(range(1, 10))
        right_wall = set(range(18, 82, 9))  # Starts from 18 because the corner overlaps with top_wall
        bottom_wall = set(range(73, 81))
        left_wall = set(range(10, 65, 9))

        inner_walls = {21, 23, 25, 39, 41, 43, 57, 59, 61}

        self.assert_wall(top_wall, walls, "Top")
        self.assert_wall(right_wall, walls, "Right")
        self.assert_wall(bottom_wall, walls, "Bottom")
        self.assert_wall(left_wall, walls, "Left")
        self.assert_wall(inner_walls, walls, "Inner")

        self.assertEqual(len(walls), 0, f"Following walls not tested:\n\n{walls}")

    def test_size(self):
        self.assertEqual(9, self.map.size, "Map size (square dimensions)")

    def test_chars(self):
        self.assertEqual(self.map.chars[0], None, "Tile ID 0 shall be None")
        self.assertTrue(self.map.chars[1] == 'X' or self.map.chars[1] == '#', "Tile ID 1 shall be a wall")
        self.assertTrue(self.map.chars[11] == '@', f"Tile ID 11 shall be a robot but is '{self.map.chars[11]}' instead")


class TestMap02(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # Gets executed before all of the tests
        cls.parser = MapParser()  # "cls.parser" is a class variable (shared across all instances)
        cls.map = cls.parser.parse("D:/Users/imbrm/GitHub/ITU/AdvancedRobotics/maps/map_02_two_cans.txt")

    def test_goals(self):
        self.assertEqual([15, 51], self.map.goals)

    def test_cans(self):
        self.assertEqual([15, 31], self.map.cans)

    def test_robot(self):
        self.assertEqual([71], self.map.robot)

    def assert_wall(self, wall_to_assert, walls, wall_name):
        set_diff = wall_to_assert.difference(walls)
        self.assertTrue(len(set_diff) == 0, f"{wall_name} wall parsed\n\n{set_diff} not in\n{walls}")
        [walls.remove(wall) for wall in wall_to_assert]  # Remove wall

    def test_walls(self):
        TestMap01.test_walls(self)


class TestMap03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # Gets executed before all of the tests
        cls.parser = MapParser()  # "cls.parser" is a class variable (shared across all instances)
        cls.map = cls.parser.parse("D:/Users/imbrm/GitHub/ITU/AdvancedRobotics/maps/map_03_robot_on_goal.txt")

    def test_goals(self):
        self.assertEqual([15, 51], self.map.goals)

    def test_cans(self):
        self.assertEqual([15, 31, 53, 65], self.map.cans)

    def test_robot(self):
        self.assertEqual([51], self.map.robot)

    def assert_wall(self, wall_to_assert, walls, wall_name):
        set_diff = wall_to_assert.difference(walls)
        self.assertTrue(len(set_diff) == 0, f"{wall_name} wall parsed\n\n{set_diff} not in\n{walls}")
        [walls.remove(wall) for wall in wall_to_assert]  # Remove wall

    def test_walls(self):
        TestMap01.test_walls(self)


class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        cls.parser = MapParser()  # "cls.parser" is a class variable (shared across all instances)
        cls.map = cls.parser.parse("D:/Users/imbrm/GitHub/ITU/AdvancedRobotics/maps/MAP_COMPETITION.txt")
        cls.solver = Solver(cls.map)
        cls.solution = cls.solver.solve(False, False)

    def test_outputAction(self):
        self.assertEqual(self.solution.outputActions(), [0, 0, -1, -90, 90, 90, 0, -1])
        # print(self.solution.outputActions())

if __name__ == "__main__":
    unittest.main()
