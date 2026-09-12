# 6-Axis Robot Torque Calculator v3

Streamlit-based torque calculator for a 6-axis manipulator.

## Features

- 6 configurable axes;
- adjustable joint angles;
- link length, mass and center of mass (`com`) for each link;
- configurable payload mass;
- simplified static gravity torque calculation for all joints;
- safety factor;
- required torque at gearbox output;
- motor + gearbox selection from candidate tables;
- interactive SVG diagram of the robot arm with dimensions.

## Run

```bash
start.bat
```

Requires a shared virtual environment at `..\venv`.

## Important

The current calculation is a **planar static first-approximation model**. It does not replace a full Newton-Euler / spatial dynamic analysis of an industrial robot.

Motor and gearbox values in `app.py` are for demonstration only. Do not use them for equipment procurement.

## Where to change parameters

All robot parameters are entered interactively in the Streamlit sidebar:

- link lengths, masses and COM positions;
- payload mass;
- joint angles;
- safety factor.

Motor and gearbox options are defined in `app.py` (`MOTOR_OPTIONS`, `GEARBOX_OPTIONS`).
=======
# 6-Axis-Robot-Torque-Calculator
