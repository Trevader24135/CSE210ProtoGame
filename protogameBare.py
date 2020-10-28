import sys
sys.path.append('pygame_engines')
import math
import time

from pgRenderer import pgRenderer
import RayCasterBare as RayCaster
import VectorOps
import ListOps
import mapTools
import entities
import GUI

FOV = 100
width = 800
height = 600
supersampling = 3

FOV *= math.pi / 180
cameraDist = 0.1 / math.tan(FOV / 2)

class Player(entities.Object):
    def __init__(self):
        super().__init__(position = [3.5,3.5])
        self.direction = VectorOps.normalize((-1,0))

class Game:
    def __init__(self):
        self._running = True
        self.keysHeld = []
        self.rayCaster = RayCaster.Screen(mapTools.map, width = width, height = height, supersampling = supersampling, cameraDist = cameraDist, debug = False)
        self.loopTime, self.fpsTime = 0, 0
        self.player = Player()
        self.enemies = [
            entities.Goblin(position = [7.8,3.9]),
            entities.Goblin(position = [7.8,5.1])
        ]

        self.screen = pgRenderer(800, 600)
        
    def on_event(self, event):
        if event[0] == 'QUIT':
            self._running = False
        elif event[1] == 'press' and not event[0] in self.keysHeld:
            self.keysHeld.append(event[0])
        elif event[1] == 'release' and event[0] in self.keysHeld:
            self.keysHeld.remove(event[0])
    
    def loop(self):
        def playerMovement():
            if 276 in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, -3.14 * self.deltaTime)
            elif 275 in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, 3.14 * self.deltaTime)
            if 273 in self.keysHeld:
                self.player.move(VectorOps.rotate((0,self.player.maxSpeed * self.deltaTime),VectorOps.angle(self.player.direction)))
            elif 274 in self.keysHeld:
                self.player.move(VectorOps.rotate((0,-self.player.maxSpeed * self.deltaTime),VectorOps.angle(self.player.direction)))
        
        playerMovement()

    def on_render(self):
        def generateSpriteList():
            sprites = []
            for i in self.enemies:
                spriteDist = VectorOps.distance(i.position, self.player.position)
                sprites.append([i, spriteDist])
            sprites = ListOps.sortbyindex(sprites, 1)

            for i in reversed(sprites):
                sides = VectorOps.perpendicular(VectorOps.sub(self.player.position, i[0].position), i[0].position, i[0].radius)
                spriteAngle = [VectorOps.angleWrap(VectorOps.angle(n) - VectorOps.angle(self.player.direction)) for n in VectorOps.sub(sides, self.player.position)]
                i.append(spriteAngle)
                if not ((-FOV/2 < VectorOps.angleWrap(spriteAngle[0]) < FOV/2 or -FOV/2 < VectorOps.angleWrap(spriteAngle[1]) < FOV/2) and (-1.56 < VectorOps.angleWrap(spriteAngle[0]) < 1.56 and -1.56 < VectorOps.angleWrap(spriteAngle[1]) < 1.56)):
                    sprites.remove(i)
                    continue
                if not (self.rayCaster.TestLoS(self.player.position, sides[0]) or self.rayCaster.TestLoS(self.player.position, sides[1])) or not (-FOV/2 < VectorOps.angleWrap(spriteAngle[0]) < FOV/2 or -FOV/2 < VectorOps.angleWrap(spriteAngle[1]) < FOV/2):
                    sprites.remove(i)
                    continue
            return sprites

        def drawSprites(sprites, dist = 0):
            for sprite in reversed(sprites):
                if sprite[1] > dist:
                    sprites.remove(sprite)
                    x = [int((cameraDist * math.tan(n) * 10 + 1) * width / 2) for n in sprite[2]]
                    spriteDist = (sprite[1] - (cameraDist / math.cos((sprite[2][0] + sprite[2][1]) / 2))) * math.cos((sprite[2][0] + sprite[2][1]) / 2) #transform to non-euclidean
                    spriteHeight = int(((height / 2) * sprite[0].height)/(spriteDist))
                    spriteCorners = [x[0], (height / 2) + (height / 4)/(spriteDist) - spriteHeight, x[1] - x[0], int(((height / 2) * sprite[0].height)/(spriteDist))]
                    if spriteCorners[2] > width:
                        continue
                    self.screen.drawSprite(sprite[0].sprite, spriteCorners, sprite[1])
            return sprites

        rays = self.rayCaster.RaySweep(self.player.position,self.player.direction)
        polygons = self.rayCaster.RenderSweep(rays, sort=True)

        sprites = generateSpriteList()

        self.screen.drawBG()

        for i in reversed(polygons):
            sprites = drawSprites(sprites, i[0])
            self.screen.drawWall(mapTools.numToColor(mapTools.map[i[2][0]][i[2][1]], i[3]), i[1], i[0])
        drawSprites(sprites)

        self.screen.update()

    def timer(self):
        self.deltaTime = time.perf_counter() - self.loopTime
        self.loopTime = time.perf_counter()
        self.fpsTime += self.loopTime
        if self.fpsTime > 100:
            print("FPS:", round(1/self.deltaTime,1))
            self.fpsTime = 0

    def on_execute(self):
        while( self._running ):
            self.timer()
            for i in self.screen.events():
                self.on_event(i)
            self.loop()
            self.on_render()

def mainLaunch(renderer = ''):
    controller = Game()
    controller.on_execute()

if __name__ == "__main__":
    mainLaunch()