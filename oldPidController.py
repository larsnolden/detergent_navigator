from PIDPATH.main import PIDCoords
from simple_pid import PID
import math

class PidController:
    KP = 2.5
    KI = 0.2
    KD = 10


    def __init__(self):
        self.pidStraight = PID(self.KPstraight, self.KIstraight, self.KDstraight)
        self.idealPath = PIDCoords(resolution='cm')
        self.pid = PID(self.KP, self.KI, self.KD, setpoint=1)
        self.pid.output_limits = (-255, 255)

        print("Pid controller setup done!")

    # Steer strength R[-255, 255]
    def getSteer(self, position):
        shiftX = 0
        xPos = round(position["x"]-shiftX, 1)
        if xPos > 340: return 0
        if xPos < -34: raise ValueError("Ran out of coordinates");
        
        yRef = self.idealPath.getY(xPos)
        self.pid.setpoint = yRef
        steer = int(self.pid(position["y"]))
        return steer

    def getXY(self):
        return self.idealPath.getAll()
