import render
import sys
import math
import random

import numpy as np
from tensorflow import keras
model = keras.models.load_model('lastmodel')

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))



class CollisionResolve:

    def __init__(self, body1, body2):
        self.input = [body1.x / 340.0, body1.y / 480.0, body1.radius / 15.0, body2.x / 340.0, body2.y/480.0, body2.radius / 15.0]
        self.output = []
    
    def RegisterResolve(self, body1, body2):
        self.output = [body1.x / 340.0, body1.y / 480.0, body2.x / 340.0, body2.y / 480.0]

class PhysSolver2d:

    def __init__(self) -> None:
        self.bodies = []
        self.resolves = []
        
        pass

        
    def Render(self, window : render.Window):
        for b in self.bodies:
            window.DrawCricle((b.x, b.y), b.radius, render.GRAY)
            if b.collidedThisFrame:
                window.DrawCricle((b.x, b.y), b.radius - 2.0, render.RED)
            else:
                window.DrawCricle((b.x, b.y), b.radius - 2.0, b.color)

    def Update(self, dt):
        for b in self.bodies:
            b.ResetForNewFrame()
        
        steps = 8
        step_dt = dt / float(steps)
        self.Step(step_dt)

    def Step(self, dt):
        for x in range(0, len(self.bodies) - 1):
            body1 = self.bodies[x]
            for y in range(x + 1, len(self.bodies)):
                body2 = self.bodies[y]
                if body1.Collides(body2):
                    self.Resolve(body1, body2)  

    def Resolve(self, body1, body2):
        learning = False
        if learning:
            resolve = CollisionResolve(body1, body2)
            
            distance = math.sqrt(math.pow(body1.x - body2.x, 2) + math.pow(body1.y - body2.y, 2))
            
            if abs(distance) <= 0.001:
                distance = 0.001

            depth = (distance - body1.radius - body2.radius)
            
            normalX = (body2.x - body1.x) / distance
            normalY = (body2.y - body1.y) / distance

            body1.x += normalX * depth
            body1.y += normalY * depth

            body2.x -= normalX * depth
            body2.y -= normalY * depth

            body1.x = clamp(body1.x, 20.0, 460.0)
            body2.x = clamp(body2.x, 20.0, 460.0)
            body1.y = clamp(body1.y, 20.0, 320.0)
            body2.y = clamp(body2.y, 20.0, 320.0)
            
            resolve.RegisterResolve(body1, body2)

            self.resolves.append(resolve)
        else:
            X = np.array([body1.x / 340.0, body1.y / 480.0, body1.radius / 15.0, body2.x / 340.0, body2.y / 480.0, body2.radius / 15.0])
            X = np.expand_dims(X,axis=0)
            Y = model.predict(X, verbose=0)
            body1.x = Y[0][0] * 340.0
            body1.y = Y[0][1] * 480.0
            body2.x = Y[0][2] * 340.0
            body2.y = Y[0][3] * 480.0

        body1.x = clamp(body1.x, 20.0, 460.0)
        body2.x = clamp(body2.x, 20.0, 460.0)
        body1.y = clamp(body1.y, 20.0, 320.0)
        body2.y = clamp(body2.y, 20.0, 320.0)

class RigidCircleBody2d:
    def __init__(self, x, y, radius, color) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.collidedThisFrame =  False
        
    def ResetForNewFrame(self):
        self.collidedThisFrame =  False

    def Collides(self, other) -> bool:
        distanceSq = math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2)
        if distanceSq <= math.pow(self.radius + other.radius, 2):
            other.collidedThisFrame = True
            self.collidedThisFrame = True
            return True
        
        return False

def lerp(a : float, b : float, t : float) -> float:
    return a * (1.0 - t) + (b * t)


def StartSimulation():
    window = render.Window(480, 360, "2d Phys Simulation Circles")
    solver = PhysSolver2d()

    player_circle = RigidCircleBody2d(window.width / 4, window.height / 2, 10, render.BLUE)
    solver.bodies.append(player_circle)

    for i in range(100):
        x = random.randrange(30, window.width - 30)
        y = random.randrange(30, window.height - 30)
        r = random.randrange(5, 15)
        solver.bodies.append(RigidCircleBody2d(x, y, r, render.GREEN))

    dt = 1.0 / window.fps

    speed = 0.0
    MaxSpeed = 250.0
    simulate = False
    iterations = 0
    while not window.controls.quit:
        window.Clear()
        window.Update()

        keydown = False
        if window.controls.left:
            keydown = True
            player_circle.x -= speed * dt
        if window.controls.right:
            keydown = True
            player_circle.x += speed * dt
        if window.controls.up:
            keydown = True
            player_circle.y -= speed * dt
        if window.controls.down:
            keydown = True
            player_circle.y += speed * dt
        
        if keydown:
            speed = lerp(speed, MaxSpeed, dt * 2)
        else:
            speed = lerp(speed, 25.0, dt * 20)

        solver.Update(dt)
        solver.Render(window)

        window.Render()

        iterations += 1
        if iterations % 60 == 0:
            print("Numer of resolves = ", len(solver.resolves))

        if len(solver.resolves) > 1000000 or window.controls.space:
            break
  
    if window.controls.quit:
        sys.exit(-1)
    original_stdout = sys.stdout # Save a reference to the original standard output

    with open('input.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        for r in solver.resolves:
            print(r.input[0],", ", r.input[1],", ", r.input[2],", ", r.input[3],", ", r.input[4],", ", r.input[5])

    with open('output.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        for r in solver.resolves:
            print(r.output[0],", ", r.output[1],", ", r.output[2],", ", r.output[3])
        
    sys.stdout = original_stdout
StartSimulation()