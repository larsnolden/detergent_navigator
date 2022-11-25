import gopigo as go
from simple_pid import PID


print("Script is starting")
pid = PID(1, 0.1, 0.05, setpoint=1)
pid.output_limits = (0, 255)

def locationEstimation():
    x = 0.5
    y = 0.2
    return {x, y}


def path(x):
    return 1



while True:
    x_loc, y_loc = locationEstimation()
    y_ref = path(x_loc)
    #error = y_loc - y_ref

    # set the desired value (setpoint)
    pid.setpoint = y_ref
    corrective_steering = pid(y_loc)

    # print("Motor 2 moving forward at full speed")
    # gopigo.motor2(1,255)

    # steer right if error is positive
    # steer left if error is negative
    # combined_motor_speed = 2 * 255;
    # make right motor spin faster to turn left
    # make left motor spin faster to turn right
    right_motor_speed = combined_motor_speed - 
    go.motor1(1, )
