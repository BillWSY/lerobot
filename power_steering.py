from lerobot.common.robot_devices.motors.configs import FeetechMotorsBusConfig
from lerobot.common.robot_devices.motors.utils import make_motors_bus
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus
import time

def make_arm(port: str = "/dev/ttyACM0"):
    return make_motors_bus(
        "feetech",
        port=port,
        motors={
            # name: (index, model)
            "shoulder_pan": [1, "sts3215"],
            "shoulder_lift": [2, "sts3215"],
            "elbow_flex": [3, "sts3215"],
            "wrist_flex": [4, "sts3215"],
            "wrist_roll": [5, "sts3215"],
            "gripper": [6, "sts3215"],
        }
    )

def main():
    arm = make_arm()
    arm.connect()
    arm.write("Torque_Enable", 0)

    motor_id = 6

    arm.write_with_motor_ids(arm.motor_models, motor_id, "Mode", 2)
    arm.write_with_motor_ids(arm.motor_models, motor_id, "Torque_Enable", 0)
    arm.write_with_motor_ids(arm.motor_models, motor_id, "Torque_Limit", 50)

    next_time = time.time()
    next_action_time = next_time
    last_pos = arm.read_with_motor_ids(arm.motor_models, motor_id, "Present_Position")
    while True:
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        iter_start_time = time.time()
        next_time = iter_start_time + 0.1
        next_action_time = max(next_action_time, iter_start_time)

        speed = arm.read_with_motor_ids(arm.motor_models, motor_id, "Present_Speed")
        pos = arm.read_with_motor_ids(arm.motor_models, motor_id, "Present_Position")
        if (pos > 32768):
            pos = - (pos - 32768)
        if (speed > 32768):
            speed = - (speed - 32768)
        print(f'Pos: {pos}, speed: {speed}')

        control = speed * 10
        if control > 10: control = 10
        if control < -10: control = -10

        arm.write_with_motor_ids(arm.motor_models, motor_id, "Goal_Time", control)
        print(f'Control: {control}')


if __name__ == "__main__":
    main()
