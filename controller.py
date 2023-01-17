from pidController import PidController
from visualizer import Visualizor
from cameraPos import cameraPos
from encoderPos import encoderPos
import gopigo as go
# from sim import Simulator
import math

class Controller:
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
    totalDistanceTraveled = {
        "left": 0,
        "right": 0
    }

    def __init__(self, debug=False):
        # self.go = Simulator(0.01)
        self.pidController = PidController()
        self.viz = Visualizor(self.pidController.getXY())
        # Initializing encoder tracker with current position (offsetting)
        print("Controller setup complete!")

    def run(self):
        go.set_left_speed(self.MAX_SPEED)
        go.set_right_speed(self.MAX_SPEED)
        go.fwd()
        self.viz.update(self.getCenterPosition(), self.wheelPositions, 0, self.totalDistanceTraveled, [0, 0])

        while True:
            

    
    def stop(self):
        go.stop()

    # Steer the car
    def steer(self, steerStrength):
        if steerStrength == 0:
            return

        # Positive steer, go right, decrease throttle on left wheels
        if steerStrength > 0:
            go.set_left_speed(self.MAX_SPEED)
            go.set_right_speed(self.MAX_SPEED - steerStrength)
        # Negative steer, go left, reduce throttle on left wheels
        else:
            go.set_left_speed(self.MAX_SPEED + steerStrength)
            go.set_right_speed(self.MAX_SPEED)



        




    