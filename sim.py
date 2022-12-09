import time
import math

class Simulator: 
    motorSpeed = {
        "left": 0,
        "right": 0
    }
    ENC_STEPSIZE = 19.63/18
    TIME_STEP = 0.1 # time increments per step
    encoderSteps = {
        0: 0,
        1: 0
    }
    position = {
        "x": 340,
        "y": 0
    }
    wheelPositions = {
        "left": {
            "x": 340.0,
            "y": -6
        },
        "right": {
            "x": 340.0,
            "y": 6
        }
    }
    totalDistances = {
        "left": 0,
        "right": 0
    }
    running = 1
    

    def __init__(self, tickSpeed):
        self.tickSpeed = tickSpeed

    def set_left_speed(self, newSpeed):
        if(newSpeed > 255) or (newSpeed < 1):
            return print("Invalid speed!", newSpeed)
        self.motorSpeed["left"] = newSpeed

    def set_right_speed(self, newSpeed):
        if(newSpeed > 255) or (newSpeed < 1):
            return print("Invalid speed!", newSpeed)
        self.motorSpeed["right"] = newSpeed

    def print_motor_speeds(self):
        print("motor Speeds: ", self.motorSpeed)

    def fwd(self):
        print("Moving...")
        self.running = 1
        return
    
    def stop(self):
        print("Stopping...")
        self.running = 0
        return

    def enc_read(self, leftOrRight):
        return self.encoderSteps[leftOrRight]
    
    def tick(self):
        time.sleep(self.tickSpeed)
        # print('-' * 10)
        leftMove = 255/self.motorSpeed["left"] * self.TIME_STEP * self.ENC_STEPSIZE
        rightMove = 255/self.motorSpeed["right"] * self.TIME_STEP * self.ENC_STEPSIZE

        # Perpendicular vector of the vector between wheel right and left
        xPerpendicularVector = -(self.wheelPositions["right"]["y"] - self.wheelPositions["left"]["y"])
        yPerpendicularVector = self.wheelPositions["right"]["x"] - self.wheelPositions["left"]["x"]

        # print("Xfactor = ", (self.wheelPositions["right"]["x"] - self.wheelPositions["left"]["x"]))
        # print("Yfactor = ", (self.wheelPositions["right"]["y"] - self.wheelPositions["left"]["y"]))
        # print("perpendicular: ", xPerpendicularVector, yPerpendicularVector)

        # Distance between wheels is 12cm, so the vector is also of length 12
        xUnitVector = xPerpendicularVector/12
        yUnitVector = yPerpendicularVector/12

        # print(" addition vector L:", xUnitVector * leftMove, yUnitVector * leftMove)
        # print(" addition vector R:", xUnitVector * rightMove, yUnitVector * rightMove)

        # if xUnitVector == 0.0:
        #     xUnitVector += 0.01
        # if yUnitVector == 0.0:
        #     yUnitVector += 0.01
        # print("before wheel positions: ", self.wheelPositions)

        # Distance traveled (cm) * unitvector gives the movement per axis
        self.wheelPositions["left"]["x"] += xUnitVector * leftMove
        self.wheelPositions["left"]["y"] += yUnitVector * leftMove
        self.wheelPositions["right"]["x"] += xUnitVector * rightMove
        self.wheelPositions["right"]["y"] += yUnitVector * rightMove

        # do A wheel correction cuz idk, float rounding errors or sth
        XdiffVector = self.wheelPositions["right"]["x"] - self.wheelPositions["left"]["x"]
        YdiffVector = self.wheelPositions["right"]["y"] - self.wheelPositions["left"]["y"]

        dist = math.sqrt(XdiffVector**2 + YdiffVector**2)
        if dist != 12:
            newXPos = XdiffVector / dist * 12
            newYPos = YdiffVector / dist * 12
            self.wheelPositions["right"]["x"] = self.wheelPositions["left"]["x"] + newXPos
            self.wheelPositions["right"]["y"] = self.wheelPositions["left"]["y"] + newYPos

        xLeftWheelToCenterVector = (self.wheelPositions["right"]["x"] - self.wheelPositions["left"]["x"]) / 2
        yLeftWheelToCenterVector = (self.wheelPositions["right"]["y"] - self.wheelPositions["left"]["y"]) / 2

        self.position = {
            "x": self.wheelPositions["left"]["x"] + xLeftWheelToCenterVector,
            "y": self.wheelPositions["left"]["y"] + yLeftWheelToCenterVector
        }

        self.totalDistances["left"] += leftMove
        self.totalDistances["right"] += rightMove

        # print("leftMoved: ", leftMove, "RightMoved:", rightMove)
        # print("motorSpeeds:", self.motorSpeed)
        # print("new position: ", self.position)
        # print("encoder steps: ", self.encoderSteps)
        # print("totaldistances: ", self.totalDistances)
        # print("Unit vector: ", xUnitVector, yUnitVector)
        # print("wheel positions: ", self.wheelPositions)

        self.encoderSteps[0] = math.floor(self.totalDistances["left"])
        self.encoderSteps[1] = math.floor(self.totalDistances["right"])


