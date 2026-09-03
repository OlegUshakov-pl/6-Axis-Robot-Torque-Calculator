from config import SAFETY_FACTOR
from robot import Robot
from dynamics import gravity_torque, required_torque
from motors import select_motor_and_gearbox


def main():
    robot = Robot()

    # Example pose. Angles are relative joint angles in degrees.
    angles = [0, 30, -20, 10, 15, 0]

    torques = gravity_torque(robot, angles)

    print("=== O1 Torque Calculator ===")
    print(f"Axes: {robot.axes}")
    print(f"Total mass: {robot.total_mass():.2f} kg")
    print(f"Safety factor: {SAFETY_FACTOR:.2f}\n")
    print("JOINT   GRAVITY    DESIGN TORQUE   MOTOR/GEARBOX")
    print("--------------------------------------------------")

    for i, torque in enumerate(torques):
        design = required_torque(torque)
        choice = select_motor_and_gearbox(design)
        if choice:
            pair = f'{choice["motor"]["name"]} + {choice["gearbox"]["name"]}'
        else:
            pair = "No candidate"
        print(f"J{i+1:<5} {torque:>7.2f} Nm   {design:>9.2f} Nm   {pair}")


if __name__ == "__main__":
    main()
