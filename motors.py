from config import MOTOR_OPTIONS, GEARBOX_OPTIONS


def motor_output_torque(motor_nm, ratio, efficiency):
    return motor_nm * ratio * efficiency


def required_motor_torque(output_torque, ratio, efficiency):
    return output_torque / (ratio * efficiency)


def select_motor_and_gearbox(required_output_nm):
    candidates = []
    for gearbox in GEARBOX_OPTIONS:
        for motor in MOTOR_OPTIONS:
            output = motor_output_torque(
                motor["continuous_nm"], gearbox["ratio"], gearbox["efficiency"]
            )
            if output >= required_output_nm:
                candidates.append((output, motor, gearbox))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0])
    output, motor, gearbox = candidates[0]
    return {
        "motor": motor,
        "gearbox": gearbox,
        "available_output_nm": output,
    }
