# navigation.py  (Group A - Navigation & Sensing)
# Drive, turn and obstacle-detection functions (distances in mm).
# Ports: distance = PORT1, left = PORT2, right = PORT3

from vex import *
import time

brain = Brain()

distance_sensor = DistanceSensor(Ports.PORT1)

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)

WHEEL_CIRCUMFERENCE_MM = 320
STOP_DISTANCE_MM = 200


def stop_motors():
    left_motor.stop()
    right_motor.stop()


def move_forward(distance_mm, speed=70):
    rotations = distance_mm / WHEEL_CIRCUMFERENCE_MM
    left_motor.spin_for(FORWARD, rotations, TURNS, speed, VelocityUnits.PERCENT)
    right_motor.spin_for(FORWARD, rotations, TURNS, speed, VelocityUnits.PERCENT)
    stop_motors()


def turn_right(angle_deg):
    turn_rot = angle_deg / 90.0 * 0.5
    left_motor.spin_for(FORWARD, turn_rot, TURNS, 50, VelocityUnits.PERCENT)
    right_motor.spin_for(REVERSE, turn_rot, TURNS, 50, VelocityUnits.PERCENT)
    stop_motors()


def obstacle_detected():
    return distance_sensor.distance(DistanceUnits.MM) < STOP_DISTANCE_MM
