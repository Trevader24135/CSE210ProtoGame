import sys
sys.path.append('pygame_engines')

import VectorOps
import pgRenderer as Renderer
from mapTools import map

class Object:
    def __init__(self, position = [0,0], velocity = [0,0], sprite = "", health = 100, radius = 0.25, height = 2/3, speed = 1):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.sprite = sprite
        self.health = health
        self.height = height #height is in terms of walls
        self.maxSpeed = speed

    def move(self, direction):
        def mapRel(direction):
            return map[int(self.position[0]) + direction[0]][int(self.position[1]) + direction[1]]
        
        def checkCollision(direction): #run 2 checks in each direction, at each side of the player
            if direction[0] > 0 and type(mapRel((1,0))) != int and VectorOps.fpart(self.position[0]) > 1 - self.radius:
                direction[0] = 0
            elif direction[0] < 0 and type(mapRel((-1,0))) != int and VectorOps.fpart(self.position[0]) < self.radius:
                direction[0] = 0
            if direction[1] > 0 and type(mapRel((0,1))) != int and VectorOps.fpart(self.position[1]) > 1 - self.radius:
                direction[1] = 0
            elif direction[1] < 0 and type(mapRel((0,-1))) != int and VectorOps.fpart(self.position[1]) < self.radius:
                direction[1] = 0
            return direction
        
        direction = checkCollision(direction)
        self.position = [i + direction[j] for j,i in enumerate(self.position)]

class Goblin(Object):
    def __init__(self, position = [3.5, 3.5]):
        super().__init__(position = position, sprite = Renderer.goblinSprite, height = 1/2)
