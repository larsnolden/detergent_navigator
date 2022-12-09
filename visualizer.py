import pygame

class Visualizor:
    offset = 200
    optimalPath = []

    def __init__(self, optimalpath):
        pygame.init()
        for x in optimalpath:
            self.optimalPath.append([x, self.offset+optimalpath[x]])
        self.screen = pygame.display.set_mode([500, 500])
        self.screen.fill((255, 255, 255))
        print("Simulator initialized!")

    def update(self, botPosition, wheelPositions, steerStrength):
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 print("event happened, quit")
        self.screen.fill((255, 255, 255))
        self.drawTargetPath()
        self.drawRobot(botPosition, wheelPositions)
        self.drawSteerBar(steerStrength)
        pygame.display.flip()

    def drawRobot(self, pos, wheels):
        #body
        pygame.draw.circle(self.screen, pygame.Color("black"), (pos["x"], self.offset+pos["y"]), 5)
        pygame.draw.circle(self.screen, pygame.Color("black"), (pos["x"], self.offset+pos["y"]), 10)
        #wheels
        pygame.draw.circle(self.screen, pygame.Color("green"), (wheels["left"]["x"], self.offset+wheels["left"]["y"]), 5)
        pygame.draw.circle(self.screen, pygame.Color("green"), (wheels["right"]["x"], self.offset+wheels["right"]["y"]), 5)

    def drawTargetPath(self):
        pygame.draw.lines(self.screen, pygame.Color("red"), False, self.optimalPath, 1)

    def drawSteerBar(self, steerStrength):
        pygame.draw.rect(self.screen, pygame.Color("red"), pygame.Rect(128, 30, 255, 30))
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect(255 + (steerStrength / 2), 34, 10, 28))