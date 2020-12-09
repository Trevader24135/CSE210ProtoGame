import sys
sys.path.append('pygame_engines')
import time

import pgRenderer as Renderer
import VectorOps

#used for pathfinding/movement
from mapTools import map
import heapq

class MobAI:
    def __init__(self, mapdata):
        self.pathingSubSampling = 3
        self.mapoffset = 2
        self.pathoffset = 1
        mapEnlargened = []
        for y in mapdata:
            row = []
            for x in y:
                if type(x) == int:
                    for i in range(self.pathingSubSampling):
                        row.append(0)
                else:
                    for i in range(self.pathingSubSampling):
                        row.append(1)
            for i in range(self.pathingSubSampling):
                mapEnlargened.append(row)
        #for i in mapEnlargened:
        #    print(i)
        #print()
        self.map = mapEnlargened
        self.map = [[1 for i in range(self.mapoffset)] + n for n in self.map]
        self.map = [[1 for i in range(len(self.map[0]))] for i in range(self.mapoffset)] + self.map
        #for i in self.map:
        #    print(i)
    
    def findPath(self, start, goal):
        start = (int(start[0] * self.pathingSubSampling), int(start[1] * self.pathingSubSampling))
        goal = (int(goal[0] * self.pathingSubSampling) + self.pathoffset, int(goal[1] * self.pathingSubSampling) + self.pathoffset)

        def heuristic(a, b):
            return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)**(1/2) #straight line score from current to goal

        neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)] #possible tile movements, one for each direction
        close_set = set() #initialize close set
        came_from = {} #
        gscore = {start:0} #gscore is the cheapest path from start to current currently known
        fscore = {start:heuristic(start, goal)} #fscore is the best-case score if start goes through current
        oheap = [] #
        heapq.heappush(oheap, (fscore[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]
            if current == goal: #if we have reached the goal
                data = [] #reconstruct the path from start to goal
                while current in came_from:
                    data.append(VectorOps.divide(current,self.pathingSubSampling))
                    current = came_from[current]
                data += [VectorOps.divide(start,self.pathingSubSampling)] #add start to the path
                return data[::-1] #return reconstructed path (reversed, so start is first)

            close_set.add(current)
            for i, j in neighbors: #test every neighbor
                neighbor = current[0] + i, current[1] + j #set current neighbor to the current position plus neighbor offset
                tentative_g_score = gscore[current] + heuristic(current, neighbor) #set the estimated gscore to current's gscore plus this neighbor's score
                if 0 <= neighbor[0] < len(self.map): #cancel if this neighbor is outside of Y bounds
                    if 0 <= neighbor[1] < len(self.map[0]): #cancel if this neighbor is outside of X bounds
                        if type(self.map[neighbor[0]][neighbor[1]]) == 1: #cancel if this neighbor is not open space
                            continue
                    else:
                        continue
                else:
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0): #if this neighbor is already in close_set with a lower or equal score
                    continue

                if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        return False # no path available

class Object:
    def __init__(self, position = [0,0], velocity = [0,0], sprite = "", radius = 0.25, height = 2/3, speed = 1):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.sprite = sprite
        self.height = height #height is in terms of walls
        self.maxSpeed = speed
        self.colorMultiplier = [1,1,1]
        self.colorAniTime = 0

    def move(self, direction, collideWithEntities=False, normalizeResult=False, smoothCollision=False):#direction is a vector with a direction(angle) and magnitude(speed)
        def mapRel(direction):
            return map[int(self.position[0] + direction[0])][int(self.position[1] + direction[1])]
        magnitude = VectorOps.length(direction)

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
        def checkCollisionSmooth(direction):
            if direction[0] > 0 and type(mapRel((1,0))) != int and VectorOps.fpart(self.position[0]) > 1 - self.radius:
                direction[0] = 0
            elif direction[0] < 0 and type(mapRel((-1,0))) != int and VectorOps.fpart(self.position[0]) < self.radius:
                direction[0] = 0
            if direction[1] > 0 and type(mapRel((0,1))) != int and VectorOps.fpart(self.position[1]) > 1 - self.radius:
                direction[1] = 0
            elif direction[1] < 0 and type(mapRel((0,-1))) != int and VectorOps.fpart(self.position[1]) < self.radius:
                direction[1] = 0
            return direction
        def checkEntities(direction):
            return direction

        if smoothCollision:
            direction = checkCollisionSmooth(direction)
        else:
            direction = checkCollision(direction)
        if normalizeResult:
            direction = VectorOps.multiply(VectorOps.normalize(direction), magnitude)

        if collideWithEntities:
            direction = checkEntities(direction)

        self.position = [i + direction[j] for j,i in enumerate(self.position)]
        return direction

class Character(Object):# vv                                      Object Info                                                   vv  vv                     Character Stats                     vv
    def __init__(self, position = [0,0], velocity = [0,0], sprite = "", radius = 0.25, height = 2/3, speed = 1, entityList = None, health = 100, currentHealth = 100, defense = 10, attackDamage = 100, reach = 0.75):
        super().__init__(position = position, velocity = velocity, sprite = sprite, radius = radius, height = height, speed = speed)
        self.destination = [1,1]
        self.health = health
        self.defense = defense
        self.attackDamage = attackDamage
        self.reach = reach
        self.currentHealth = currentHealth
        self.entityList = entityList
        self.attackCoolDown = 0.4 #attack cool down duration in seconds
        self.attackTime = 0 #time of last attack

    def attack(self, target):
        self.attackTime = time.perf_counter()
        damageDealt = target.damage(self.attackDamage)
        return damageDealt

    def damage(self, damage):
        self.colorMultiplier = [255, 0.5, 0.5]
        self.colorAniTime = time.perf_counter() + 0.150

        if(self.defense < damage):
            self.currentHealth -= damage - self.defense

        print(self.currentHealth)

        if(self.currentHealth <= 0):
            self.entityList.remove(self)
        
        return damage - self.defense

## Specific Entity Types ##

class Player(Character):
    def __init__(self, position, direction=(-1,0)):
        super().__init__(position)
        self.direction = VectorOps.normalize(direction)
        self.walking = False
        self.attacking = False
        self.attackHit = False

class Goblin(Character):
    def __init__(self, position = [3.5, 3.5], entityList = None):
        super().__init__(position = position, sprite = Renderer.goblinSprite, height = 1/2, entityList = entityList, speed=0.3)
