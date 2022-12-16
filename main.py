import time
import traceback

from controller import Controller
import pygame
from gopigo import stop
# from PIDPATH.generator import generateFile
import sys

if __name__ == "__main__":
    # pygame.init()
    # screen = pygame.display.set_mode([500, 500])
    # screen.fill((255, 255, 255))
    # pygame.display.flip()
    # while True:
    #     screen.fill((255, 255, 255))
    #     pygame.display.update()
    #     time.sleep(1)
    # screen.fill((255, 255, 255))
    # pygame.display.flip()
    # generateFile('./PID_PATH.svg')
    controller = Controller()
    try:
        controller.run()
    except Exception as e:
        stop()
        print("Crashed")
        print(e)
        traceback.print_exc()
        stop()
    #except Exception as e:
    #     print("Program crashed, stopped bot!")
    #     print(e)
    #     controller.stop()
    #     sys.exit(-1)