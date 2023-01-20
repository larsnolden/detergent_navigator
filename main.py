import time
import traceback

from controller import Controller
import pygame
# from gopigo import stop
# from PIDPATH.generator import generateFile
import sys

if __name__ == "__main__":
    controller = Controller()
    try:
        controller.run()
    except Exception as e:
        # stop()
        print("Crashed")
        print(e)
        traceback.print_exc()
        # stop()