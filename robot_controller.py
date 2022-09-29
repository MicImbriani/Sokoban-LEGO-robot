from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor)
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.nxtdevices import LightSensor


# Controls the low-level actions of the robot
# (e.g. sets the speed and direction of the motors)


class RobotController:
    def __init__(self):
        # ==================================== Settings
        # self.crossDistance = 30 # testing
        self.crossDistance = 50
        self.intersection_threshold = 15

        # self.follow_speed = 20 # testing
        self.follow_speed = 110
        self.backup_distance = -60

        self.follow_sensitivity = 0.3

        # ==================================== Setup
        self.sensM = LightSensor(Port.S2)
        self.sensL = ColorSensor(Port.S1)
        self.sensR = ColorSensor(Port.S3)

        self.error = 0
        self.motorB = Motor(Port.B)  # RIGHT
        self.motorA = Motor(Port.A)  # LEFT

        # Initialize the drive base.
        self.driveBase = DriveBase(
            self.motorB, self.motorA, wheel_diameter=42, axle_track=190)
        self.driveBase.settings(1500, 500, 100, 100)

        self.ev3 = EV3Brick()

    def execute_path(self, action_list):  # ========================== Main code
        i = 0

        while i < len(action_list):
            action = action_list[i]

            if action == -1:  # PUSH
                self.crossTape()
                self.followLine(self.follow_speed,
                                self.follow_sensitivity, midpoint=50)

                if action_list[i + 1] == 0:
                    i += 1
                else:
                    self.back_up()

            else:
                if not (i == 0):
                    self.crossTape()
                self.rotate(-action) if action != 0 else None
                self.followLine(self.follow_speed,
                                self.follow_sensitivity, midpoint=50)
                self.ev3.speaker.beep(1000, 500)

            i += 1

    def followLine(self, speed, sensitivity=1, midpoint=50):
        while self.detectCrossSection() == False:
            self.error = self.sensM.reflection() - midpoint
            self.driveBase.drive(speed, self.error * sensitivity)

    def crossTape(self):
        self.driveBase.straight(self.crossDistance)

    def driveStraight(self, distanceMM):
        self.driveBase.straight(distanceMM)

    def turnLeft(self):
        self.crossTape()
        self.driveBase.turn(90)

    def turnRight(self):
        self.crossTape()
        self.driveBase.turn(-90)

    def rotate(self, angle):
        self.driveBase.turn(angle)

    def printSensorReadings(self):
        message = "L: " + str(self.sensL.reflection())
        message += "  M: " + str(self.sensM.reflection())
        message += "  R: " + str(self.sensR.reflection())
        print(message)

    def back_up(self):
        # self.driveBase.drive(200, 150)
        self.driveBase.straight(self.backup_distance)
        self.rotate(180)
        self.followLine(self.follow_speed,
                        self.follow_sensitivity, midpoint=50)

        self.ev3.speaker.beep(1000, 500)

    def detectCrossSection(self):
        line_l = self.sensL.reflection() < self.intersection_threshold
        line_r = self.sensR.reflection() < self.intersection_threshold
        return line_l or line_r

    # def update(self):
    #     line_following_speed = 260
    #     rotation_speed = 200
    #
    #     self.followLine(line_following_speed,
    #                     self.follow_sensitivity, midpoint=50)
    #     self.printSensorReadings()
    #
    #     line_l = self.sensL.reflection() < 15
    #     line_r = self.sensR.reflection() < 15
    #
    #     if line_l or line_r:
    #         self.driveStraight(10)
    #
    #     line_l = self.sensL.reflection() < 15
    #     line_r = self.sensR.reflection() < 15
    #
    #     if line_l and line_r:  # T junction
    #         self.turnRight()
    #     elif line_l and (not line_r):  # Left turn
    #         self.turnLeft()
    #     elif (not line_l) and line_r:  # Right turn
    #         self.turnRight()
