import RPi.GPIO as GPIO
import time
import json
from simple_pid import PID

# Motor control pins (example configuration)
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 27
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 23

# Limit switch pins
LIMIT_SWITCH_PINS = [5, 6, 13, 19, 26, 21]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
MOTOR_PINS = [MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD, MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD]
for pin in MOTOR_PINS + LIMIT_SWITCH_PINS:
    GPIO.setup(pin, GPIO.OUT if pin in MOTOR_PINS else GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Alarm state
alarm_active = False

def activate_alarm():
    global alarm_active
    alarm_active = True
    print("Alarm activated!")

def reset_alarm():
    global alarm_active
    alarm_active = False
    print("Alarm reset.")

def check_limit_switches():
    global alarm_active
    for pin in LIMIT_SWITCH_PINS:
        if not GPIO.input(pin):  # Switch is pressed
            activate_alarm()
            break

# Motor control functions
def set_motor_speed(left_speed, right_speed):
    if left_speed > 0:
        GPIO.output(MOTOR_LEFT_FORWARD, True)
        GPIO.output(MOTOR_LEFT_BACKWARD, False)
    elif left_speed < 0:
        GPIO.output(MOTOR_LEFT_FORWARD, False)
        GPIO.output(MOTOR_LEFT_BACKWARD, True)
    else:
        GPIO.output(MOTOR_LEFT_FORWARD, False)
        GPIO.output(MOTOR_LEFT_BACKWARD, False)

    if right_speed > 0:
        GPIO.output(MOTOR_RIGHT_FORWARD, True)
        GPIO.output(MOTOR_RIGHT_BACKWARD, False)
    elif right_speed < 0:
        GPIO.output(MOTOR_RIGHT_FORWARD, False)
        GPIO.output(MOTOR_RIGHT_BACKWARD, True)
    else:
        GPIO.output(MOTOR_RIGHT_FORWARD, False)
        GPIO.output(MOTOR_RIGHT_BACKWARD, False)

# YOLO processing
def process_yolo_output(json_data):
    """
    Process YOLO output to find the center x of the target.
    """
    objects = json.loads(json_data)
    largest_box = max(objects, key=lambda box: (box[2] - box[0]) * (box[3] - box[1]), default=None)

    if largest_box:
        center_x = (largest_box[0] + largest_box[2]) / 2
        center_y = (largest_box[1] + largest_box[3]) / 2
        return center_x, center_y
    return None, None

# PID Controller
pid = PID(0.1, 0.01, 0.05, setpoint=0)  # Tune Kp, Ki, Kd values
pid.output_limits = (-100, 100)  # Motor speed range

def main():
    global alarm_active
    try:
        while True:
            check_limit_switches()

            if alarm_active:
                print("In alarm mode. Reset to continue.")
                time.sleep(1)
                continue

            # Simulated YOLO output (replace with real YOLO data)
            yolo_json = '[{"x_min": 5.24, "y_min": 6.53, "x_max": 15.234, "y_max": 71.234}]'
            target_x, target_y = process_yolo_output(yolo_json)

            if target_x is not None:
                screen_center = 320  # Assuming a 640px wide screen
                offset = target_x - screen_center

                # PID adjustment
                pid_output = pid(offset)

                # Adjust motor speeds for turning
                left_motor_speed = -pid_output
                right_motor_speed = pid_output

                set_motor_speed(left_motor_speed, right_motor_speed)

            else:
                print("No target detected.")
                set_motor_speed(0, 0)

            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
