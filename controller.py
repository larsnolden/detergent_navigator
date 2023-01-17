from pidController import PidController
from visualizer import Visualizor
from cameraPos import cameraPos
from encoderPos import encoderPos
from stateMachine import stateMachine
import gopigo as go
# from sim import Simulator
import math

class Controller:
    DIST_WHEEL_TO_CENTER = 10/2 #cm
    MAX_SPEED = 100
    position = {
        "x": 0,
        "y": 350
    }

    def __init__(self, debug=False):
        # self.go = Simulator(0.01)
        self.pidController = PidController()
        self.viz = Visualizor(self.pidController.getXY())
        self.encoder = encoderPos(self.viz)
        self.camera = cameraPos(self.viz)
        self.statemachine = stateMachine(self.viz)
        # Initializing encoder tracker with current position (offsetting)
        print("Controller setup complete!")

    def run(self):
        go.set_left_speed(self.MAX_SPEED)
        go.set_right_speed(self.MAX_SPEED)
        go.fwd()
        # self.viz.update(self.getCenterPosition(), self.wheelPositions, 0, self.totalDistanceTraveled, [0, 0])

        while True:
            # update encoder position
            encoderPos = self.encoder.run()
            # get the camera angle and perceived position
            cameraPos, angle = self.camera.run(self.stateMachine.getState(), position)
            self.steer(pid.getSteer(position))
            if cameraPos is not None:
                self.encoder.correctPosition(cameraPos, angle)
            
            steerStrength = self.pidController.getSteer(self.encoder.getCenterPosition()['x'])
            self.viz.setSteerStrength(steerStrength)
            self.steer(steerStrength)
            self.viz.display()
    
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



        




    