# pick_place.py  (Group B - Section 5)
# Pick-up (lower -> close -> lift) and placement (lower -> open -> lift)
# sequences with Brain screen feedback.
# Ports: arm = PORT4, claw = PORT5

from vex import *

brain = Brain()

arm_motor = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
claw_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)

ARM_LOWER_POS = 0
ARM_LIFT_POS = 90
CLAW_OPEN_POS = 0
CLAW_CLOSE_POS = 60

def lower_arm():
    arm_motor.spin_to_position(
        ARM_LOWER_POS,
        RotationUnits.DEG,
        60,
        VelocityUnits.PERCENT,
        True
    )
    brain.screen.next_row()
    brain.screen.print("Arm Lowered")

def close_claw():
    claw_motor.spin_to_position(
        CLAW_CLOSE_POS,
        RotationUnits.DEG,
        60,
        VelocityUnits.PERCENT,
        True
    )
    brain.screen.next_row()
    brain.screen.print("Claw Closed")

def lift_arm():
    arm_motor.spin_to_position(
        ARM_LIFT_POS,
        RotationUnits.DEG,
        60,
        VelocityUnits.PERCENT,
        True
    )
    brain.screen.next_row()
    brain.screen.print("Arm Lifted")

def open_claw():
    claw_motor.spin_to_position(
        CLAW_OPEN_POS,
        RotationUnits.DEG,
        60,
        VelocityUnits.PERCENT,
        True
    )
    brain.screen.next_row()
    brain.screen.print("Claw Opened")

def execute_pick():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Pick Sequence")

    lower_arm()
    close_claw()
    lift_arm()

def execute_place():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Place Sequence")

    lower_arm()
    open_claw()
    lift_arm()

arm_motor.set_position(0, RotationUnits.DEG)
claw_motor.set_position(0, RotationUnits.DEG)
