import sys

sys.path.append('pygame_engines')

import pgRenderer as Renderer
import VectorOps

from mapTools import map

class MobAI:
    def __init__(self):
        pass

    def pathing(self, mobs):
        for i in mobs:
            pass #for every mob, 1) determine if a target has been seen 2) determine the correct direction to reach the target 3) move the mob towards the target
            
class Object:
    def __init__(self, position = [0,0], velocity = [0,0], sprite = "", radius = 0.25, height = 2/3, speed = 1):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.sprite = sprite
        self.height = height #height is in terms of walls
        self.maxSpeed = speed

    def move(self, direction):
        def mapRel(direction):
            return map[int(self.position[0] + direction[0])][int(self.position[1] + direction[1])]
        
        def checkCollision(direction): #run 2 checks in each direction, at each side of the player
            if direction[0] > 0:
                if  VectorOps.fpart(self.position[0]) > 1 - self.radius:
                    if type(mapRel((1, self.radius))) != int or type(mapRel((1, -self.radius))) != int:
                        direction[0] = 0

            elif direction[0] < 0: 
                if VectorOps.fpart(self.position[0]) < self.radius:
                    if type(mapRel((-1, self.radius))) != int or type(mapRel((-1, -self.radius))) != int:
                        direction[0] = 0

            if direction[1] > 0: 
                if VectorOps.fpart(self.position[1]) > 1 - self.radius:
                    if type(mapRel((self.radius,1))) != int or type(mapRel((-self.radius,1))) != int:
                        direction[1] = 0

            elif direction[1] < 0: 
                if VectorOps.fpart(self.position[1]) < self.radius:
                    if type(mapRel((self.radius,-1))) != int or type(mapRel((-self.radius,-1))) != int:
                        direction[1] = 0

            return direction
        
        direction = checkCollision(direction)
        self.position = [i + direction[j] for j,i in enumerate(self.position)]

class Character(Object):# vv                                  Object Info                                               vv  vv                     Character Stats                     vv
    def __init__(self, position = [0,0], velocity = [0,0], sprite = "", radius = 0.25, height = 2/3, speed = 1, entityList = None, health = 100, currentHealth = 100, defense = 10, attackDamage = 100, reach = 0.75):
        super().__init__(position = position, velocity = velocity, sprite = sprite, radius = radius, height = height, speed = speed)
        self.health = health
        self.defense = defense
        self.attackDamage = attackDamage
        self.reach = reach
        self.currentHealth = currentHealth

    def attack(self, target):
        target.damage(self.attackDamage)

    def damage(self, damage):

        if(self.defense < damage):
            self.currentHealth -= damage - self.defense

        print(self.currentHealth)

        if(self.currentHealth <= 0):
            print("Death!!!")
            self.entityList.remove(self)

## Specific Entity Types ##

class Player(Character):
    def __init__(self):
        super().__init__(position = [3.5,3.5])
        self.direction = VectorOps.normalize((-1,0))
        self.walking = False

        

class Goblin(Character):
    def __init__(self, position = [3.5, 3.5], entityList = None):
        super().__init__(position = position, sprite = Renderer.goblinSprite, height = 1/2, entityList = entityList)
