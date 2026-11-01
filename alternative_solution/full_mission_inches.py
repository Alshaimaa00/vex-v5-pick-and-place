# full_mission_inches.py
# Standalone full mission written as a single program (distances in inches):
# drive -> grab -> avoid obstacles -> find drop-off -> release -> return to start.
# NOTE: different port layout from the integrated robot:
#   left = PORT1, right = PORT5, claw = PORT3, arm = PORT4, distance = PORT10

from vex import *
import math

brain = Brain()

left_drive = Motor(Ports.PORT1, False)
right_drive = Motor(Ports.PORT5, True)
claw_motor = Motor(Ports.PORT3, False)
arm_motor = Motor(Ports.PORT4, False)
front_distance = Distance(Ports.PORT10)

WHEEL_CIRCUMFERENCE_IN = 200 / 25.4
TRACK_WIDTH_IN = 8.0
TURN_CALIBRATION = 2.25

DRIVE_SPEED = 40
TURN_SPEED = 30
ARM_SPEED = 35
CLAW_SPEED = 35

OBJECT_DISTANCE_IN = 10
OBSTACLE_DISTANCE_IN = 3

AVOID_FORWARD_IN = 12
DROPOFF_RELEASE_DISTANCE_IN = 10
DROPOFF_STEP_IN = 5

CLAW_OPEN_DEG = 0
CLAW_CLOSED_DEG = 90
ARM_DOWN_DEG = 0
ARM_UP_DEG = 310

movement_log = []
total_forward_inches = 0


def status(text):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(text)


def setup_robot():
    left_drive.set_stopping(BRAKE)
    right_drive.set_stopping(BRAKE)
    claw_motor.set_stopping(HOLD)
    arm_motor.set_stopping(HOLD)

    left_drive.set_velocity(DRIVE_SPEED, PERCENT)
    right_drive.set_velocity(DRIVE_SPEED, PERCENT)
    claw_motor.set_velocity(CLAW_SPEED, PERCENT)
    arm_motor.set_velocity(ARM_SPEED, PERCENT)

    left_drive.reset_position()
    right_drive.reset_position()
    claw_motor.set_position(CLAW_OPEN_DEG, DEGREES)
    arm_motor.set_position(ARM_DOWN_DEG, DEGREES)


def wheel_degrees_for_inches(inches):
    return (inches / WHEEL_CIRCUMFERENCE_IN) * 360


def wheel_degrees_for_turn(angle_degrees):
    turn_arc_inches = math.pi * TRACK_WIDTH_IN * (angle_degrees / 360)
    return wheel_degrees_for_inches(turn_arc_inches) * TURN_CALIBRATION


def wait_for_drive():
    while left_drive.is_spinning() or right_drive.is_spinning():
        wait(0.02, SECONDS)


def save_starting_point():
    global movement_log, total_forward_inches
    movement_log = []
    total_forward_inches = 0
    status("Start saved")


def move_forward(inches, speed=DRIVE_SPEED, record=True):
    global total_forward_inches

    degrees = wheel_degrees_for_inches(inches)
    left_drive.set_velocity(speed, PERCENT)
    right_drive.set_velocity(speed, PERCENT)

    left_drive.spin_for(FORWARD, degrees, DEGREES, wait=False)
    right_drive.spin_for(FORWARD, degrees, DEGREES, wait=False)
    wait_for_drive()

    if record:
        movement_log.append(("drive", inches))
        total_forward_inches += inches


def move_reverse(inches, speed=DRIVE_SPEED, record=True):
    degrees = wheel_degrees_for_inches(inches)
    left_drive.set_velocity(speed, PERCENT)
    right_drive.set_velocity(speed, PERCENT)

    left_drive.spin_for(REVERSE, degrees, DEGREES, wait=False)
    right_drive.spin_for(REVERSE, degrees, DEGREES, wait=False)
    wait_for_drive()

    if record:
        movement_log.append(("drive", -inches))


def turn_left(angle, speed=TURN_SPEED, record=True):
    degrees = wheel_degrees_for_turn(angle)
    left_drive.set_velocity(speed, PERCENT)
    right_drive.set_velocity(speed, PERCENT)

    left_drive.spin_for(REVERSE, degrees, DEGREES, wait=False)
    right_drive.spin_for(FORWARD, degrees, DEGREES, wait=False)
    wait_for_drive()

    if record:
        movement_log.append(("turn", -angle))


def turn_right(angle, speed=TURN_SPEED, record=True):
    degrees = wheel_degrees_for_turn(angle)
    left_drive.set_velocity(speed, PERCENT)
    right_drive.set_velocity(speed, PERCENT)

    left_drive.spin_for(FORWARD, degrees, DEGREES, wait=False)
    right_drive.spin_for(REVERSE, degrees, DEGREES, wait=False)
    wait_for_drive()

    if record:
        movement_log.append(("turn", angle))


def front_inches():
    if front_distance.is_object_detected():
        return front_distance.object_distance(INCHES)
    return 999


def open_claw():
    status("Open claw")
    claw_motor.spin_to_position(CLAW_OPEN_DEG, DEGREES, CLAW_SPEED, PERCENT, wait=True)
    claw_motor.stop(HOLD)


def close_claw():
    status("Grab object")
    claw_motor.spin_to_position(CLAW_CLOSED_DEG, DEGREES, CLAW_SPEED, PERCENT, wait=True)
    claw_motor.stop(HOLD)


ARM_LIFT_DIRECTION = FORWARD
ARM_LOWER_DIRECTION = REVERSE
ARM_LIFT_TIME = 1.2
ARM_LOWER_TIME = 1.0

DROPOFF_FOUND_MIN_IN = 45
DROPOFF_FOUND_MAX_IN = 55


def lift_object_and_hold():
    status("Lift object")
    arm_motor.set_velocity(20, PERCENT)
    arm_motor.spin(ARM_LIFT_DIRECTION)
    wait(ARM_LIFT_TIME, SECONDS)
    arm_motor.stop(HOLD)


def lower_arm_for_drop():
    status("Lower arm")
    arm_motor.set_velocity(45, PERCENT)
    arm_motor.spin(ARM_LOWER_DIRECTION)
    wait(ARM_LOWER_TIME, SECONDS)
    arm_motor.stop(HOLD)


def grab_object():
    status("Grab object")
    close_claw()
    wait(0.3, SECONDS)
    lift_object_and_hold()
    wait(0.3, SECONDS)


def avoid_obstacle():
    status("Avoid obstacle")

    turn_left(90)
    move_forward(10)

    turn_right(90)
    move_forward(12)

    turn_right(90)
    move_forward(10)

    turn_left(90)


def move_until_dropoff_found():
    status("Carry object")

    while True:
        distance = front_inches()

        if distance <= 10:
            avoid_obstacle()

        elif DROPOFF_FOUND_MIN_IN <= distance <= DROPOFF_FOUND_MAX_IN:
            status("Dropoff found")
            break

        else:
            move_forward(5)


def move_close_to_dropoff():
    status("Approach dropoff")

    while True:
        distance = front_inches()

        if distance <= 10:
            break

        move_forward(5)


def drop_object():
    status("Drop object")

    lower_arm_for_drop()
    wait(0.3, SECONDS)

    open_claw()
    wait(0.3, SECONDS)

    lift_object_and_hold()


def return_to_start():
    status("Return start")

    for move in reversed(movement_log):
        kind = move[0]
        value = move[1]

        if kind == "drive":
            if value > 0:
                move_reverse(value, record=False)
            else:
                move_forward(abs(value), record=False)

        elif kind == "turn":
            if value > 0:
                turn_left(value, record=False)
            else:
                turn_right(abs(value), record=False)

    status("At start")


def autonomous():
    setup_robot()
    save_starting_point()

    move_forward(10)

    grab_object()

    move_until_dropoff_found()

    move_close_to_dropoff()

    drop_object()

    return_to_start()


autonomous()