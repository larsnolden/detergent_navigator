from PIDPATH.main import PIDCoords
from simple_pid import PID
import math

class PidController:
    KP = 10
    KI = 0.3
    KD = 1.7


    def __init__(self):
        self.idealPath = PIDCoords(resolution='cm')
        self.pid = PID(self.KP, self.KI, self.KD, setpoint=1)
        self.pid.output_limits = (-255, 255)

        print("Pid controller setup done!")

    # Steer strength R[-255, 255]
    def getSteer(self, position):
        yRef = self.idealPath.getY(round(position["x"], 1))
        self.pid.setpoint = yRef
        steer = int(self.pid(position["y"]))
        return steer

    def getXY(self):
        return self.idealPath.getAll()