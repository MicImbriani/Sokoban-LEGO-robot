from sokoban.map import Map

import sys
sys.path.append('D:/Users/imbrm/GitHub/ITU/AdvancedRobotics')


class MapParser:
    @staticmethod
    def parse(map_file_path):
        goals = []
        walls = []
        cans = []
        robot = []
        size = 0

        file = open(map_file_path)
        count = 1
        chars = [None]
        static_chars = [None]

        while True:
            char = file.read(1)

            if not char:
                break
            if char == '#' or char == 'X':
                walls.append(count)
            elif char == '.':
                goals.append(count)
            elif char == '@':
                robot.append(count)
            elif char == '$':
                cans.append(count)
            elif char == '*':
                cans.append(count)
                goals.append(count)
            elif char == 'a':
                robot.append(count)
                goals.append(count)
            elif char != ' ':
                if size == 0:
                    size = count - 1
                continue

            count += 1
            chars.append(char)

            if char == '#' or char == 'X':
                static_chars.append(char)
            else:
                static_chars.append(' ')

        file.close()
        return Map(goals, walls, cans, robot, chars, static_chars, size, map_file_path)
