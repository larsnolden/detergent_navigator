from PidController import PidController
import gopigo as go

class Controller:
    DIST_WHEEL_TO_CENTER = 6
    wheelPositions = {
        "left": {
            "x": 340,
            "y": -DIST_WHEEL_TO_CENTER
        },
        "right": {
            "x": 340,
            "y": DIST_WHEEL_TO_CENTER
        }
    }
    lastEncoderValues = {
        "left": 0,
        "right": 0
    }

    def __init__(self):
        self.pidController = PidController()

    def setWheelPosition(leftOrRight='left')
        perpendicularVector = {
            "x": -(self.wheelPositions["left"]["y"] - self.wheelPositions["left"]["y"]),
            "y": self.wheelPositions["right"]["x"] - self.wheelPositions["right"]["x"]
        }
        # perpendicularY = currentRightWheelPos["x"] - currentLeftWheelPos["x"]
    # while True:


    