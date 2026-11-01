# integrated_robot.py
# Full Autonomous Pick-and-Place System
# Merges Group A (navigation & sensing) and Group B (manipulation & control).
# Routine: navigate -> avoid obstacle -> pick -> transport -> place

from vex import *
import time


# ---- Hardware Setup (from both groups) ----
brain = Brain()
distance_sensor = DistanceSensor(Ports.PORT1)
left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
arm_motor = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
claw_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)


# ---- Navigation Constants & Functions (Group A) ----
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


# ---- Manipulation Constants & Functions (Group B) ----
ARM_LOWER_POS = 0
ARM_LIFT_POS = 90
CLAW_OPEN_POS = 0
CLAW_CLOSE_POS = 60


def lower_arm():
    arm_motor.spin_to(ARM_LOWER_POS, DEGREES, 60, VelocityUnits.PERCENT)


def lift_arm():
    arm_motor.spin_to(ARM_LIFT_POS, DEGREES, 60, VelocityUnits.PERCENT)


def close_claw():
    claw_motor.spin_to(CLAW_CLOSE_POS, DEGREES, 60, VelocityUnits.PERCENT)


def open_claw():
    claw_motor.spin_to(CLAW_OPEN_POS, DEGREES, 60, VelocityUnits.PERCENT)


def execute_pickup():
    lower_arm()
    time.sleep(0.5)
    close_claw()
    time.sleep(0.5)
    lift_arm()
    brain.screen.print("Object secured")


def execute_placement():
    lower_arm()
    time.sleep(0.5)
    open_claw()
    time.sleep(0.5)
    lift_arm()
    brain.screen.print("Object placed")


# ---- Full Autonomous Routine ----
def full_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Starting full auto...")

    # Navigate to pickup
    move_forward(500)
    if obstacle_detected():
        turn_right(45)
        move_forward(300)
    move_forward(800)

    # Pickup
    execute_pickup()
    time.sleep(1)

    # Navigate to drop
    turn_right(90)
    move_forward(1000)

    # Placement
    execute_placement()

    brain.screen.print("Mission complete")


if __name__ == "__main__":
    full_autonomous()
