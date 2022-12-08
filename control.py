import gopigo as go #the dependencie of the gopigo file should resolve if ran on the Dexter Image
from simple_pid import PID
from PIDPATH.generator import generateFile
from PIDPATH.main import PIDCoords


# import importlib.util
# import sys
# spec = importlib.util.spec_from_file_location("di_i2c", "./Dexter/lib/Dexter/RFR_Tools/miscellaneous/di_i2c.py")
# di_i2c = importlib.util.module_from_spec(spec)
# sys.modules["di_i2c"] = di_i2c 
# spec.loader.exec_module(di_i2c)

# # ugly import of gopygo library (not available via pip)
# spec = importlib.util.spec_from_file_location("gopigo", "./Dexter/GoPiGo/Software/Python/gopigo.py")
# go = importlib.util.module_from_spec(spec)
# sys.modules["gopigo"] = go 
# spec.loader.exec_module(go)

print("Script is starting")

## Setup path
# generates a csv file with raw and cleaned coordinates inside /pidpathData by default
#generateFile('./path_images/PID_PATH.svg')
# resolutions (mm(default), cm, m), has the optional paramters xOffset and yOffset and filename for cleaned svg
ideal_path= PIDCoords(resolution='mm')

# get limits on x axis
max_x = ideal_path.getMaxX()
min_x = ideal_path.getMinX()


## Setup PID
Kp = 1
Ki = 0.1
Kd = 0.05
pid = PID(Kp, Ki, Kd, setpoint=1)
combined_motor_speed = 2*255; #both motors go full force
pid.output_limits = (-255, 255)

def locationEstimation():
    x = 401 
    y = -600
    return [x, y]

# set the both motors to start speed
go.set_speed(10)

while True:
    x_loc, y_loc = locationEstimation()
    y_ref = ideal_path.getY(x_loc)
    error = y_loc - y_ref
    print('error: %s', error)

    # set the desired value (setpoint)
    pid.setpoint = y_ref
    corrective_steering = pid(y_loc)
    print('corrective_steering: %s', corrective_steering)

    if(corrective_steering > 0):
        # steer left
        go.set_right_speed(corrective_steering)
        go.set_left_speed(100 - corrective_steering)
    elif(corrective_steering < 0):
        # steer right
        go.set_right_speed(100 - corrective_steering*(-1))
        go.set_left_speed(corrective_steering*(-1))

# while True:
#     x_loc, y_loc = locationEstimation()
#     y_ref = ideal_path.getY(x_loc)
#     error = y_loc - y_ref
#     print('error: %s', error)

#     # set the desired value (setpoint)
#     pid.setpoint = y_ref
#     corrective_steering = pid(y_loc)
#     print('corrective_steering: %s', corrective_steering)
#     exit

    # print("Motor 2 moving forward at full speed")
    # gopigo.motor2(1,255)

    # steer right if error is negative
    # steer left if error is positive
    # therefore the negative amount is 
    # each motor has a max motor speed of 255

    # make right motor spin faster to turn left
    # make left motor spin faster to turn right
    # right_motor_speed = combined_motor_speed - 0
    # go.motor1(1, )

