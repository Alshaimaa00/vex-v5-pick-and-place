# pick_place_logged.py  (Group B - Task 6)
# Pick-up and placement sequences that also log how long each action takes.
# Ports: arm = PORT4, claw = PORT5

from vex import *
import time

brain = Brain()

arm_motor = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
claw_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)

ARM_LOWER_POS = 0
ARM_LIFT_POS = 90
CLAW_OPEN_POS = 0
CLAW_CLOSE_POS = 60

pickup_success = False
log_data = []


def add_log(action, start_time, end_time):
    duration = end_time - start_time
    log_data.append({
        "action": action,
        "duration_sec": round(duration, 2)
    })


def lower_arm():
    start = time.time()
    arm_motor.spin_to(ARM_LOWER_POS, DEGREES, 60, VelocityUnits.PERCENT)
    end = time.time()
    add_log("Lower Arm", start, end)


def close_claw():
    start = time.time()
    claw_motor.spin_to(CLAW_CLOSE_POS, DEGREES, 60, VelocityUnits.PERCENT)
    end = time.time()
    add_log("Close Claw", start, end)


def lift_arm():
    start = time.time()
    arm_motor.spin_to(ARM_LIFT_POS, DEGREES, 60, VelocityUnits.PERCENT)
    end = time.time()
    add_log("Lift Arm", start, end)


def open_claw():
    start = time.time()
    claw_motor.spin_to(CLAW_OPEN_POS, DEGREES, 60, VelocityUnits.PERCENT)
    end = time.time()
    add_log("Open Claw", start, end)


def execute_pickup():
    lower_arm()
    close_claw()
    lift_arm()


def execute_placement():
    lower_arm()
    open_claw()
    lift_arm()
