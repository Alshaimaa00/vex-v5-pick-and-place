# arm_claw_calibration.py  (Group B - Task 4)
# Calibrates arm and claw zero positions, then tests directions and limits.
# Ports: arm = PORT1, claw = PORT2 (test rig; the integrated robot uses PORT4/PORT5)

from vex import *

brain = Brain()

arm_motor = Motor(Ports.PORT1, GearSetting.RATIO_36_1, False)
claw_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

ARM_MIN = 0
ARM_MAX = 200
CLAW_OPEN = 0
CLAW_CLOSED = 60

def calibrate_manipulator():

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    arm_motor.set_max_torque(40, PercentUnits.PERCENT)
    claw_motor.set_max_torque(40, PercentUnits.PERCENT)

    arm_motor.set_position(0, RotationUnits.DEG)
    claw_motor.set_position(0, RotationUnits.DEG)
    wait(1, TimeUnits.SEC)

    brain.screen.next_row()
    brain.screen.print("Arm Zero = 0 deg")
    brain.screen.next_row()
    brain.screen.print("Claw Zero = 0 deg")
    wait(2, TimeUnits.SEC)

def move_arm(position):

    if position < ARM_MIN:
        position = ARM_MIN

    if position > ARM_MAX:
        position = ARM_MAX

    arm_motor.spin_to_position(
        position,
        RotationUnits.DEG,
        30,
        VelocityUnits.PERCENT,
        True
    )
def move_claw(position):

    if position < CLAW_OPEN:
        position = CLAW_OPEN
    if position > CLAW_CLOSED:
        position = CLAW_CLOSED
    claw_motor.spin_to_position(
        position,
        RotationUnits.DEG,
        30,
        VelocityUnits.PERCENT,
        True )

def test_directions():

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Direction Test")
    brain.screen.next_row()
    brain.screen.print("Arm Up")
    move_arm(100)

    wait(1, TimeUnits.SEC)

    brain.screen.next_row()
    brain.screen.print("Arm Down")
    move_arm(0)

    wait(1, TimeUnits.SEC)

    brain.screen.next_row()
    brain.screen.print("Claw Close")
    move_claw(CLAW_CLOSED)

    wait(1, TimeUnits.SEC)

    brain.screen.next_row()
    brain.screen.print("Claw Open")
    move_claw(CLAW_OPEN)

    wait(1, TimeUnits.SEC)

def test_limits():

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Testing Limits")

    move_arm(ARM_MAX)
    wait(1, TimeUnits.SEC)

    move_arm(ARM_MIN)
    wait(1, TimeUnits.SEC)

    move_claw(CLAW_CLOSED)
    wait(1, TimeUnits.SEC)

    move_claw(CLAW_OPEN)
    wait(1, TimeUnits.SEC)

    brain.screen.next_row()
    brain.screen.print("Limits OK")

def display_positions():

    brain.screen.clear_screen()

    brain.screen.set_cursor(1, 1)
    brain.screen.print("Arm:")

    brain.screen.print(
        arm_motor.position(RotationUnits.DEG))

    brain.screen.print(" deg")
    brain.screen.next_row()
    brain.screen.print("Claw:")
    brain.screen.print(
        claw_motor.position(RotationUnits.DEG)
    )

    brain.screen.print(" deg")

    wait(3, TimeUnits.SEC)

calibrate_manipulator()
test_directions()
test_limits()

display_positions()
brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
