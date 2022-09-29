class Map:
    def __init__(self, goals, walls, cans, robot, chars, static_chars, size: int, map_file_path: str):
        self.goals = goals
        self.walls = walls
        self.cans = cans
        self.robot = robot
        self.chars = chars
        self.static_chars = static_chars
        self.size = size
        self.map_file_path = map_file_path
