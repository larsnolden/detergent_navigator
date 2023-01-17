from pidController import PidController
from visualizer import Visualizor
import gopigo as go
# from sim import Simulator
import math

class encodePos:
    DIST_WHEEL_TO_CENTER = 10/2 #cm
    ENC_STEPSIZE = 20.73/18 #cm/step of the encoder
    MAX_SPEED = 100
    wheelPositions = {
        "left": {
            "x": 340.0,
            "y": -DIST_WHEEL_TO_CENTER
        },
        "right": {
            "x": 340.0,
            "y": DIST_WHEEL_TO_CENTER
        }
    }
    lastEncoderValues = {
        "left": 0,
        "right": 0
    }
    totalDistanceTraveled = {
        "left": 0,
        "right": 0
    }

    def __init__(self, debug=False):
        # self.go = Simulator(0.01)
        self.debug = debug
        self.pidController = PidController()
        self.viz = Visualizor(self.pidController.getXY())
        # Initializing encoder tracker with current position (offsetting)
        self.lastEncoderValues["left"] = go.enc_read(0)
        self.lastEncoderValues["right"] = go.enc_read(1)
        print("Controller setup complete!")

    # update the positioning of the encoders
    def run(self):
        distanceTraveled = self.checkDisplacement()
        # No displacement, skip current loop
        if distanceTraveled["left"] + distanceTraveled["right"] == 0:
            return

        steps = 20
        for _ in range(steps):
            # Perpendicular vector of the vector between wheel right and left
            xPerpendicularVector = -(self.wheelPositions["right"]["y"] - self.wheelPositions["left"]["y"])
            yPerpendicularVector = self.wheelPositions["right"]["x"] - self.wheelPositions["left"]["x"]

            self.updateWheelPosition('left', distanceTraveled["left"]/steps, xPerpendicularVector, yPerpendicularVector)
            self.updateWheelPosition('right', distanceTraveled["right"]/steps, xPerpendicularVector, yPerpendicularVector)

    # Converting and saving a distance to x and y movement
    def updateWheelPosition(self, leftOrRight, distanceTraveled, xPerpendicularVector, yPerpendicularVector):
        if distanceTraveled == 0:
            return
        
        # Distance between wheels is 12cm, so the vector is also of length 12
        xUnitVector = xPerpendicularVector/(self.DIST_WHEEL_TO_CENTER*2)
        yUnitVector = yPerpendicularVector/(self.DIST_WHEEL_TO_CENTER*2)
        # print("Unit vector: ", xUnitVector, yUnitVector)

        # Distance traveled (cm) * unitvector gives the movement per axis
        self.wheelPositions[leftOrRight]["x"] += xUnitVector * distanceTraveled
        self.wheelPositions[leftOrRight]["y"] += yUnitVector * distanceTraveled

    def getCenterPosition(self):
        # Vector from left wheel to the center of the bot
        xLeftWheelToCenterVector = (self.wheelPositions["right"]["x"] - self.wheelPositions["left"]["x"]) / 2
        yLeftWheelToCenterVector = (self.wheelPositions["right"]["y"] - self.wheelPositions["left"]["y"]) / 2

        # 0.0 to left wheel + left wheel to center = 0.0 to center
        return {
            "x": self.wheelPositions["left"]["x"] + xLeftWheelToCenterVector,
            "y": self.wheelPositions["left"]["y"] + yLeftWheelToCenterVector
        }
    
    def checkDisplacement(self):
        # Steps taken by each encoder (1 rotation = 18 steps)
        leftEncoder = go.enc_read(0)
        rightEncoder = go.enc_read(1)

        # Distance traveled = steps taken * stepsize
        distanceTraveled = {
            "left": (leftEncoder - self.lastEncoderValues["left"]) * self.ENC_STEPSIZE,
            "right": (rightEncoder - self.lastEncoderValues["right"]) * self.ENC_STEPSIZE
        }
        self.totalDistanceTraveled["left"] += distanceTraveled["left"]
        self.totalDistanceTraveled["right"] += distanceTraveled["right"]

        self.lastEncoderValues["left"] = leftEncoder
        self.lastEncoderValues["right"] = rightEncoder

        return distanceTraveled



        




    