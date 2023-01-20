from pidController import PidController
from visualizer import Visualizor
from cameraPos import cameraPos
from encoderPos import encoderPos
from stateMachine import stateMachine
# from PIDPATH.main import PIDCoords
from bottlePositions import bottlePositions
# import gopigo as go
from sim import Simulator
import math
import time

class Controller:
    DIST_WHEEL_TO_CENTER = 10/2 #cm
    MAX_SPEED = 100
    position = {
        "x": 340,
        "y": 0
    }

    def __init__(self, debug=False):
        self.pidController = PidController()
        self.viz = Visualizor(self.pidController.getXY(), self.pidController.getPID())
        self.go = Simulator(0.01, self.viz)
        self.encoder = encoderPos(self.viz, self.go)
        self.camera = cameraPos(self.viz)
        self.statemachine = stateMachine(self.viz)
        # Initializing encoder tracker with current position (offsetting)
        print("Controller setup complete!")

    def run(self):
        # self.go.set_left_speed(self.MAX_SPEED)
        # self.go.set_right_speed(self.MAX_SPEED)
        # self.initial_turn()
        # self.go.stop()
        # time.sleep(5)
        self.go.fwd()
        self.go.set_left_speed(self.MAX_SPEED)
        self.go.set_right_speed(self.MAX_SPEED)
        self.go.fwd()
        # self.viz.update(self.getCenterPosition(), self.wheelPositions, 0, self.totalDistanceTraveled, [0, 0])
        self.viz.setBotPosition(self.encoder.getCenterPosition(), self.encoder.wheelPositions)
        # self.maxX = PIDCoords(cleanedCSV="./pidpathDataL3/output_clean.csv", resolution='cm').getMaxX()
        self.maxX = bottlePositions.getBottlePositions()[0]['x']

        while True:
            # update encoder position
            self.go.tick()
            self.viz.displayText(self.pidController.getPID())
            encoderPos = self.encoder.run()
            print(f"encoder pos: {encoderPos}")
            # get the camera angle and perceived position
            cameraPos, angle = self.camera.run(self.statemachine.getState(), encoderPos)
            # if cameraPos is not None:
                # self.encoder.correctPosition(cameraPos, angle)
            print(f"camera pos: {cameraPos}")
            # if cameraPos is not None and cameraPos['y'] < 200 and cameraPos['y'] > -200:
                # camera position offsetting
                # cameraPos['y'] -= 30
                # self.encoder.correctPosition(cameraPos, angle)
                # self.viz.setCameraPos(cameraPos, angle)

            realPos = self.encoder.getCenterPosition()
            self.viz.addBotPos(realPos['x'], realPos['y'])

            steerStrength = self.pidController.getSteer(self.encoder.getCenterPosition())
            if(self.encoder.getCenterPosition()['x'] <= 15):
                while True:
                    print('end reached, stopping')
                    self.go.stop()
                
            self.viz.setSteerStrength(steerStrength)
            # self.viz.displayText(f"current state: {self.statemachine.getState()}")
            self.steer(steerStrength)
            self.viz.display()
    
    def stop(self):
        self.go.stop()

    # Steer the car
    def steer(self, steerStrength):
        if steerStrength == 0:
            return

        # Positive steer, go right, decrease throttle on right wheels
        if steerStrength > 0:
            self.go.set_left_speed(self.MAX_SPEED)
            self.go.set_right_speed(self.MAX_SPEED - steerStrength)
        # Negative steer, go left, reduce throttle on left wheels (steerstrength is negative here)
        else:
            self.go.set_left_speed(self.MAX_SPEED + steerStrength)
            self.go.set_right_speed(self.MAX_SPEED)
    
    def initial_turn(self):
        DPR = 360.0/64
        degrees = 180
        self.go.turn_right(degrees)
        self.encoder.setZero(self.go.enc_read(0), self.go.enc_read(1))
        pulse = int(degrees//DPR)
        while self.go.enc_read(0) < pulse:
            self.encoder.run()
            pass
        self.go.fwd()


        




    