# Autonomous Pick-and-Place and Navigation — VEX V5

CS1424 course project. An autonomous VEX V5 robot (Python) that navigates a course with obstacles, picks up an object, carries it to a target zone and places it.

## Team structure

| Group | Focus | Folder |
|-------|-------|--------|
| A | Navigation & sensing (movement, obstacle avoidance) | `group_a_navigation/` |
| B | Manipulation & control (arm, claw, pick/place) | `group_b_manipulation/` |
| A + B | Integration of both modules | `integration/` |

## Repository layout

```
.
├── group_a_navigation/
│   └── navigation.py             # move_forward, turn_right, obstacle_detected
├── group_b_manipulation/
│   ├── arm_claw_calibration.py   # zero positions, direction & limit tests
│   ├── pick_place.py             # pick / place sequences with screen feedback
│   └── pick_place_logged.py      # same sequences + action timing log
├── integration/
│   ├── integrated_robot.py       # main integrated program
│   └── integrated_robot_logged.py# integrated program with timing log
└── alternative_solution/
    └── full_mission_inches.py    # standalone full mission (inches, returns to start)
```

## Mission flow

`Start → Navigate → Avoid obstacle (< 200 mm → turn 45°) → Pick → Transport → Place`

## Hardware ports

| Device | Integrated robot | Calibration rig | Alternative solution |
|--------|:---:|:---:|:---:|
| Distance sensor | 1 | – | 10 |
| Left motor | 2 | – | 1 |
| Right motor | 3 | – | 5 |
| Arm motor | 4 | 1 | 4 |
| Claw motor | 5 | 2 | 3 |

## Running

1. Open [VEXcode V5](https://www.vexrobotics.com/vexcode) (or the [VEXcode VR simulator](https://vr.vex.com/)) and create a Python project.
2. Paste the contents of the file you want to run (start with `integration/integrated_robot.py`).
3. Download to the V5 Brain and run.

## Contributors

- _Add names here_
