from math import radians, cos
from config import GRAVITY, SAFETY_FACTOR


def gravity_torque(robot, angles_deg):
    """Simplified planar static gravity torque for each joint.

    For a first engineering prototype: each joint supports all masses
    farther outboard. The full spatial Newton-Euler model can replace this later.
    """
    if len(angles_deg) != robot.axes:
        raise ValueError(f"Expected {robot.axes} joint angles")

    torques = [0.0] * robot.axes

    # For each joint, calculate the horizontal moment arm of every downstream mass.
    for j in range(robot.axes):
        cumulative = 0.0
        # Contribution from downstream link COMs.
        for i in range(j, robot.axes):
            arm = 0.0
            cumulative = 0.0
            for k in range(j, i + 1):
                cumulative += angles_deg[k]
                segment = robot.links[k].com if k == i else robot.links[k].length
                arm += segment * cos(radians(cumulative))
            torques[j] += robot.links[i].mass * GRAVITY * arm

        # Payload at the end of the chain.
        payload_arm = 0.0
        cumulative = 0.0
        for k in range(j, robot.axes):
            cumulative += angles_deg[k]
            segment = robot.links[k].length
            payload_arm += segment * cos(radians(cumulative))
        torques[j] += robot.payload["mass"] * GRAVITY * payload_arm

    return torques


def required_torque(torque, safety_factor=SAFETY_FACTOR):
    return abs(torque) * safety_factor
