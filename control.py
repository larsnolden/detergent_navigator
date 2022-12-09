import gopigo as go #the dependencie of the gopigo file should resolve if ran on the Dexter Image
from simple_pid import PID
from PIDPATH.generator import generateFile
from PIDPATH.main import PIDCoords
import signal
import sys
import numpy as np

def main():
    # distanceCenterToWheel = 6
    # lastEncoderLeftValue = go.enc_read(0)
    # lastEncoderRightValue = go.enc_read(1)

    # catch sigInt (ctrl-c) to give the motors a shutdown command
    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        go.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("Script is starting")

    ## Setup path
    # generates a csv file with raw and cleaned coordinates inside /pidpathData by default
    #generateFile('./path_images/PID_PATH.svg')
    # resolutions (mm(default), cm, m), has the optional paramters xOffset and yOffset and filename for cleaned svg
    ideal_path= PIDCoords(resolution='cm')

    # get limits on x axis
    max_x = ideal_path.getMaxX()
    min_x = ideal_path.getMinX()


    ## Setup PID
    Kp = 5
    Ki = 0.0
    Kd = 1
    pid = PID(Kp, Ki, Kd, setpoint=1)
    combined_motor_speed = 2*255; #both motors go full force
    pid.output_limits = (-255, 255)

    def estimateLocationVisual():
        x = 401 
        y = -600
        return [x, y]

    distanceCenterToWheel = 6
    lastEncoderLeftValue = go.enc_read(0)
    lastEncoderRightValue = go.enc_read(1)

    currentRightWheelPos = {
        "x": 340,
        "y": 0-distanceCenterToWheel,
    }

    currentLeftWheelPos = {
        "x": 340,
        "y": 0+distanceCenterToWheel,
    }


    while True:
        wheelCircumf = 19.63 # centiMeters
        encoderStepsLeft = go.enc_read(0) - lastEncoderLeftValue
        lastEncoderLeftValue = go.enc_read(0)
        encoderStepsRight = go.enc_read(1) - lastEncoderRightValue
        lastEncoderRightValue = go.enc_read(1)
        print("encoderStepsLeft: ", encoderStepsLeft)
        print("encoderStepsRight: ", encoderStepsRight)
        print("lastEncoderLeftValue: ", lastEncoderLeftValue)
        print("lastEncoderRightValue: ", lastEncoderRightValue)

        distanceTraveledLeft = wheelCircumf*encoderStepsLeft/18
        distanceTraveledRight = wheelCircumf*encoderStepsRight/18
        ##
        perpendicularX = -(currentRightWheelPos["y"] - currentLeftWheelPos["y"])
        perpendicularY = currentRightWheelPos["x"] - currentLeftWheelPos["x"]

        # normalize
        unitVectorPerpendicular = {
            "x": perpendicularX/(distanceCenterToWheel*2),
            "y": perpendicularY/(distanceCenterToWheel*2),
        }

        currentLeftWheelPos = {
            "x": currentLeftWheelPos["x"] - unitVectorPerpendicular["x"] * distanceTraveledLeft,
            "y": currentLeftWheelPos["y"] + unitVectorPerpendicular["y"] * distanceTraveledLeft,
        }

        currentRightWheelPos = {
            "x": currentRightWheelPos["x"] - unitVectorPerpendicular["x"] * distanceTraveledRight,
            "y": currentRightWheelPos["y"] + unitVectorPerpendicular["y"] * distanceTraveledRight,
        }

        print("unitVectorPerpendicular", unitVectorPerpendicular)
        print("currentLeftWheelPos", currentLeftWheelPos)
        print("currentRightWheelPos", currentRightWheelPos)
        ##
        #vector from left to right
        vectorX = currentRightWheelPos["x"] - currentLeftWheelPos["x"]
        vectorY = currentRightWheelPos["y"] - currentLeftWheelPos["y"]
        vectorFromLeftWheelToCenter = [vectorX/2, vectorY/2] # center is half way between both wheels

        # print("Current Right Wheel Pos X: ", currentRightWheelPos["x"], "Current Right Wheel Pos Y: ", currentRightWheelPos["y"])
        # print("Current Left Wheel Pos X: ", currentLeftWheelPos["x"], "Current Right Wheel Pos Y: ", currentLeftWheelPos["y"])
        print("Vector from Left Wheel to center: ", vectorFromLeftWheelToCenter)
        
        centerPosition = [currentLeftWheelPos["x"] + vectorFromLeftWheelToCenter[0], currentLeftWheelPos["y"] + vectorFromLeftWheelToCenter[1]]

        x_loc = centerPosition[0]
        y_loc = centerPosition[1]
        print("Current position:", x_loc, y_loc)
        y_ref = ideal_path.getY(int(x_loc))
        error = int(y_loc - y_ref)
        print('error: %s', error)

        if(error == 0):
            # set the both motors to start speed
            go.set_speed(100)
            go.fwd()

        # set the desired value (setpoint)
        pid.setpoint = y_ref
        corrective_steering = int(pid(y_loc))
        print('corrective_steering: %s', corrective_steering)

        if(corrective_steering > 0):
            # steer left
            go.set_right_speed(corrective_steering)
            go.set_left_speed(100 - corrective_steering)
            go.led_on(0)
            go.led_off(1)
            go.fwd()
        elif(corrective_steering < 0):
            # steer right
            go.set_right_speed(100 - corrective_steering*(-1))
            go.set_left_speed(corrective_steering*(-1))
            go.led_on(1)
            go.led_off(0)
            go.fwd()

        print("\n", "===")

if __name__ == "__main__":
    main()
