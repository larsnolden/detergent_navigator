import pygame

class Visualizor:
    offset = 200
    optimalPath = []
    texts = []

    botPos = []
    wheelPositions = []
    perpendicularVectors = []

    def __init__(self, optimalpath):
        pygame.init()
        for x in optimalpath:
            self.optimalPath.append([x, self.offset+optimalpath[x]])
        self.screen = pygame.display.set_mode([500, 500])
        self.screen.fill((255, 255, 255))
        self.font = pygame.font.SysFont(None, 20)
        #self.surface = 
        #self.screen = pygame.transform.flip(self.screen, False, True)
        print("Simulator initialized!")
    
    def displayText(self, text):
        self.texts.append(text)
    
    def setSteerStrength(self, steerStrength):
        self.steer = steerStrength
    
    def setBotPosition(self, position, wheelPositions):
        self.botPos = position
        self.wheelPositions = wheelPositions
    
    def setVectors(self, vectors):
        self.perpendicularVectors = vectors
    
    def display(self):
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 print("event happened, quit")
        self.screen.fill((255, 255, 255))
        self.drawTargetPath()
        self.drawRobot(self.botPos, self.wheelPositions)
        self.drawSteerBar(self.steer)
        # displaying all text items
        yPos = 350
        for text in self.texts:
            self.drawText(text, 50, yPos)
            yPos += 30
        
        pygame.display.flip()

        self.resetVariables()

    def resetVariables(self):
        self.texts = []
        self.steer = 0
        self.botPos = []
        self.wheelPositions = []
        self.perpendicularVectors = []

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

    def drawRobot(self, pos, wheels):
        #body
        pygame.draw.circle(self.screen, pygame.Color("black"), (int(pos["x"]), int(self.offset+pos["y"])), 5)
        pygame.draw.circle(self.screen, pygame.Color("black"), (int(pos["x"]), int(self.offset+pos["y"])), 10)
        #wheels
        pygame.draw.circle(self.screen, pygame.Color("green"), (int(wheels["left"]["x"]), int(self.offset+wheels["left"]["y"])), 5)
        pygame.draw.circle(self.screen, pygame.Color("green"), (int(wheels["right"]["x"]), int(self.offset+wheels["right"]["y"])), 5)

    def drawTargetPath(self):
        pygame.draw.lines(self.screen, pygame.Color("red"), False, self.optimalPath, 1)

    def drawSteerBar(self, steerStrength):
        pygame.draw.rect(self.screen, pygame.Color("red"), pygame.Rect(128, 30, 255, 30))
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect(255 + int(steerStrength / 2), 34, 10, 28))