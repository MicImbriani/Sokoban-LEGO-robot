#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor)
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.nxtdevices import LightSensor

# Our modules
from robot_controller import RobotController


# save path to file

# load path from file before the main loop
rc = RobotController()
actions = [0, 0, 0, -90, -1, 0, -1, 90, -
           90, -1, -90, -1, 90, 90, 90, -1, 0, -1]

# parser = MapParser()
# map = cls.parser.parse("D:/Users/imbrm/GitHub/ITU/AdvancedRobotics/maps/mapXtest2.txt")
# solver = Solver(cls.map)
# solution = cls.solver.solve(False, False)
# actions = solution.outputActions()

# Main loop
while True:
    # UPDATE ORIENTATION OF Variable robot
    rc.execute_path(actions)
