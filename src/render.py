import pygame
from pygame.locals import *

BLACK = Color(0,   0,   0)
RED = Color(255, 0,   0)
GREEN = Color(0, 150,   0)
LIGHTGREEN = Color(0, 255,   0)
BLUE = Color(0,   0, 255)
MAGENTA = Color(255,   0, 255)
YELLOW = Color(255,   255, 0)
DARKYELLOW = Color(100,   100, 0)
TEAL = Color(0,   255, 255)
WHITE = Color(255,   255, 255)
GRAY = Color(100,   100, 100)
DARKGRAY = Color(50,   50, 50)

class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        pygame.init()
        self.displaysurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.controls = Controls()

    def SetFps(self, fps):
        self.fps = fps

    def Clear(self):
        self.displaysurface.fill(BLACK)
    
    def Update(self):
        self.controls.PollInputs()
        self.clock.tick(self.fps)

    def Exit(self):
        pygame.quit()

    def Render(self):
        pygame.display.update()
    
    def DrawCricle(self, pos, radius, color):
        pygame.draw.circle(self.displaysurface, color, pos, radius)

class Controls:
    def __init__(self) -> None:
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.space = False
        self.quit = False
    
    def PollInputs(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.down = True
                
                if event.key == pygame.K_UP:
                    self.up = True
                
                if event.key == pygame.K_RIGHT:
                    self.right = True
                
                if event.key == pygame.K_LEFT:
                    self.left = True
                
                if event.key == pygame.K_SPACE:
                    self.space = True
            
            if event.type == KEYUP:
                if event.key == pygame.K_DOWN:
                    self.down = False
                
                if event.key == pygame.K_UP:
                    self.up = False

                if event.key == pygame.K_RIGHT:
                    self.right = False
                
                if event.key == pygame.K_LEFT:
                    self.left = False
                
                if event.key == pygame.K_SPACE:
                    self.space = False
                    
            if event.type == QUIT:
                self.quit = True