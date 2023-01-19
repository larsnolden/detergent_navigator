from visualizer import Visualizor
import gopigo as go
# from sim import Simulator
import math
import time

class encoderPos:
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

    def __init__(self, visualizor):
        self.viz = visualizor
        # Initializing encoder tracker with current position (offsetting)
        self.lastEncoderValues["left"] = go.enc_read(0)
        self.lastEncoderValues["right"] = go.enc_read(1)
        print("Controller setup complete!")

    # update the positioning of the encoders
    def run(self):
        # time.sleep(0.05)
        print("cehking displacement")
        distanceTraveled = self.checkDisplacement()
        print(f"current pos: {self.getCenterPosition()}")
        print(f"dist traveled: {distanceTraveled}")
        # No displacement, skip current loop
        if distanceTraveled["left"] + distanceTraveled["right"] == 0:
            print(f"no dist traveled")
            return self.getCenterPosition()

        steps = 20
        for _ in range(steps):
            # Perpendicular vector of the vector between wheel right and left
            xPerpendicularVector = -(self.wheelPositions["right"]["y"] - self.wheelPositions["left"]["y"])
            yPerpendicularVector = self.wheelPositions["right"]["x"] - self.wheelPositions["left"]["x"]

            self.updateWheelPosition('left', distanceTraveled["left"]/steps, xPerpendicularVector, yPerpendicularVector)
            self.updateWheelPosition('right', distanceTraveled["right"]/steps, xPerpendicularVector, yPerpendicularVector)
        self.viz.setBotPosition(self.getCenterPosition(), self.wheelPositions)
        print(f"new pos: {self.getCenterPosition()}")
        return self.getCenterPosition()

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
        # time.sleep(0.02)
        rightEncoder = go.enc_read(1)
        # time.sleep(0.02)

        #if rightEncoder < self.lastEncoderValues["right"] or leftEncoder < self.lastEncoderValues["left"] or leftEncoder - self.lastEncoderValues["left"] > 18 or rightEncoder - self.lastEncoderValues["right"] > 18:
         #   print("traveled too much")
          #  return {'left': 0, 'right': 0}

        print(f"right encoder: {rightEncoder}")
        print(f"left encoder: {leftEncoder}")

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

    # # correc the encoder's position
    # def correctPosition(self, newPosition, newAngle):
    #     currentPos = self.getCenterPosition()
    #     self.wheelPositions['left']['x'] -= currentPos['x']
    #     self.wheelPositions['left']['y'] -= currentPos['y']
    #     self.wheelPositions['right']['x'] -= currentPos['x']
    #     self.wheelPositions['right']['y'] -= currentPos['y']

    #     self.wheelPositions['left']['x'] += newPosition['x']
    #     self.wheelPositions['left']['y'] += newPosition['y']
    #     self.wheelPositions['right']['x'] += newPosition['x']
    #     self.wheelPositions['right']['y'] += newPosition['y']


        # self.wheelPositions['left']['x'] += diff['x']
        # self.wheelPositions['left']['y'] += diff['y']
        # self.wheelPositions['right']['x'] -= diff['x']
        # self.wheelPositions['right']['y'] -= diff['y']


        # get the x traversal
        # xUnitVector = math.cos(newAngle-(0.5 * math.pi))
        # y value of unit circle (90 degrees backwards)
        # yUnitVector = math.sin(newAngle-(0.5 * math.pi))

        # xVector = xUnitVector * self.DIST_WHEEL_TO_CENTER
        # yVector = yUnitVector * self.DIST_WHEEL_TO_CENTER

        # self.wheelPositions['left']['x'] = newPosition['x'] - xVector
        # self.wheelPositions['left']['y'] = newPosition['y'] - yVector
        # self.wheelPositions['right']['x'] = newPosition['x'] + xVector
        # self.wheelPositions['right']['y'] = newPosition['y'] + yVector

        




    