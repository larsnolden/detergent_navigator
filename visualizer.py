import pygame
import math

class Visualizor:
    offset = 200
    optimalPath = []
    texts = []

    realPath = []
    botPath = []

    botPos = []
    camPos = None
    angle = 0
    camPos2 = None
    angle2 = 0
    wheelPositions = []
    perpendicularVectors = []

    def __init__(self, optimalpath, pid):
        pygame.init()
        for x in optimalpath:
            self.optimalPath.append([x, self.offset+optimalpath[x]])
        self.screen = pygame.display.set_mode([500, 500])
        self.screen.fill((255, 255, 255))
        self.font = pygame.font.SysFont(None, 20)
        self.f = open(f"{pid}.csv", "w")
        self.f.write(f"x,y\n")
        #self.surface = 
        #self.screen = pygame.transform.flip(self.screen, False, True)
        print("Simulator initialized!")

    def __del__(self):
        print("saving and closing file")
        self.f.close()

    def displayText(self, text):
        self.texts.append(text)
    
    def setSteerStrength(self, steerStrength):
        self.steer = steerStrength
    
    def setBotPosition(self, position, wheelPositions):
        self.botPos = position
        self.wheelPositions = wheelPositions

    def setCameraPos(self, camPos, angle):
        self.camPos = camPos
        self.angle = angle
    
    def setCameraPos2(self, camPos, angle):
        self.camPos2 = camPos
        self.angle2 = angle
    
    def setVectors(self, vectors):
        self.perpendicularVectors = vectors
    
    def display(self):
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 print("event happened, quit")
        self.screen.fill((255, 255, 255))
        self.drawTargetPath()
        self.drawRealPath()
        self.drawBotPath()
        self.drawRobot(self.botPos, self.wheelPositions)
        self.drawSteerBar(self.steer)
        self.drawCamPos(self.camPos, self.angle)
        self.drawCamPos(self.camPos2, self.angle2)
        # displaying all text items
        yPos = 350
        for text in self.texts:
            print(f"Printing {text} to Screen")
            self.drawText(text, 150, yPos)
            yPos += 15
        
        pygame.display.flip()

        self.resetVariables()

    def resetVariables(self):
        self.texts = []
        # self.steer = 0
        # self.botPos = []
        # self.wheelPositions = []
        # self.perpendicularVectors = []

    # def update(self, botPosition, wheelPositions, steerStrength, totalTraveled, pVector):
    #     for event in pygame.event.get():
    #          if event.type == pygame.QUIT:
    #              print("event happened, quit")
    #     self.screen.fill((255, 255, 255))
    #     self.drawTargetPath()
    #     self.drawRobot(botPosition, wheelPositions)
    #     self.drawSteerBar(steerStrength)
    #     self.drawText("total Traveled L:", totalTraveled["left"], 50, 450)
    #     self.drawText("total Traveled R:", totalTraveled["right"], 50, 470)
    #     self.drawText("steer str:", steerStrength, 50, 420)
    #     self.drawText("xPos:", botPosition["x"], 50, 390)
    #     self.drawText("yPos:", botPosition["y"], 50, 410)
    #     start = pVector[0] 
    #     scale = 3
    #     pygame.draw.line(self.screen, pygame.Color("red"), [botPosition["x"], self.offset+botPosition["y"]], [botPosition["x"]+pVector[0]*scale, self.offset+botPosition["y"]+pVector[1]*scale], 5)
    #     #self.screen.blit(pygame.transform.flip(self.screen, True, True), (500, 500))
    #     #self.screen = pygame.transform.flip(self.screen, True, True)
    #     pygame.display.flip()

    def drawText(self, label, xPos, yPos):
        text = self.font.render(label, True, pygame.Color("black"))
        textRect = text.get_rect()
        textRect.center = (xPos, yPos)
        self.screen.blit(text, textRect)

    def addRealPos(self, x, y):
        self.realPath.append((x,y+self.offset))

    def addBotPos(self, x, y):
        self.f.write(f"{x},{y}\n")
        self.botPath.append((x,y+self.offset))


    def drawRobot(self, pos, wheels):
        print(pos)
        print(wheels)
        if pos == [] or wheels == []:
            return
        self.texts.append(f'bot pos: x:{round(pos["x"],1)} y:{round(pos["y"],1)}')
        #body
        pygame.draw.circle(self.screen, pygame.Color("black"), (int(pos["x"]), int(self.offset+pos["y"])), 5)
        pygame.draw.circle(self.screen, pygame.Color("black"), (int(pos["x"]), int(self.offset+pos["y"])), 10)
        #wheels
        pygame.draw.circle(self.screen, pygame.Color("green"), (int(wheels["left"]["x"]), int(self.offset+wheels["left"]["y"])), 5)
        pygame.draw.circle(self.screen, pygame.Color("green"), (int(wheels["right"]["x"]), int(self.offset+wheels["right"]["y"])), 5)

    def drawCamPos(self, camPos, angle):
        if camPos is None:
            return
        self.texts.append(f'cam pos: x:{round(camPos["x"], 1)} y:{round(camPos["y"], 1)}')
        self.texts.append(f'angle: {math.degrees(angle)}')
        pygame.draw.circle(self.screen, pygame.Color("red"), (int(camPos["x"]), int(self.offset+camPos["y"])), 5)
        pygame.draw.circle(self.screen, pygame.Color("red"), (int(camPos["x"]), int(self.offset+camPos["y"])), 10)

    def drawTargetPath(self):
        pygame.draw.lines(self.screen, pygame.Color("red"), False, self.optimalPath, 1)

    def drawBotPath(self):
        if len(self.botPath) < 2:
            return
        pygame.draw.lines(self.screen, pygame.Color("green"), False, self.botPath, 1)

    def drawRealPath(self):
        if len(self.realPath) < 2:
            return
        pygame.draw.lines(self.screen, pygame.Color("blue"), False, self.realPath, 1)

    def drawSteerBar(self, steerStrength):
        pygame.draw.rect(self.screen, pygame.Color("red"), pygame.Rect(128, 30, 255, 30))
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect(255 + int(steerStrength / 2), 34, 10, 28))