import sys
sys.path.append('pygame_engines')
import config

import math
import time

import pgRenderer as Renderer
import SoundEngine
import RayCasterBare as RayCaster
import VectorOps
import ListOps
import mapTools
import entities
import GUI

FOV = 100
width = 640
height = 480
hudHeight = 100
supersampling = 4
FogofWar = 7.5


FOV *= math.pi / 180
cameraDist = 0.1 / math.tan(FOV / 2)

class Player(entities.Object):
    def __init__(self):
        super().__init__(position = [3.5,3.5])
        self.direction = VectorOps.normalize((-1,0))
        self.walking = False

class Game:
    def __init__(self):
        self.screen = Renderer.pgRenderer(width, height, cameraDist=cameraDist, FogofWar=FogofWar)
        
        self._running = True
        self.keysHeld = []
        self.rayCaster = RayCaster.Screen(mapTools.map, width = width, height = height - hudHeight, supersampling = supersampling, cameraDist = cameraDist, Renderer=self.screen)
        self.loopTime, self.fpsTime, self.fps = 0, 0, 0
        self.player = Player()
        self.enemies = [
            entities.Goblin(position = [7.8,3.9]),
            entities.Goblin(position = [7.8,5.1])
        ]
        self.gui = GUI.Hud(self.screen, self.player)

        self.soundManager = SoundEngine.SoundManager()
        self.player.walking = False
        
    def on_event(self, event):
        if event[0] == 'QUIT':
            self._running = False
        elif event[1] == 'press' and not event[0] in self.keysHeld:
            self.keysHeld.append(event[0])
        elif event[1] == 'release' and event[0] in self.keysHeld:
            self.keysHeld.remove(event[0])
    
    def loop(self):
        def playerMovement():
            if 'left' in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, -3.14 * self.deltaTime)
            elif 'right' in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, 3.14 * self.deltaTime)
            if 'up' in self.keysHeld:
                self.player.move(VectorOps.rotate((0,self.player.maxSpeed * self.deltaTime),VectorOps.angle(self.player.direction)))
                self.player.walking = 'forward'
            elif 'down' in self.keysHeld:
                self.player.move(VectorOps.rotate((0,-self.player.maxSpeed * self.deltaTime * 0.5),VectorOps.angle(self.player.direction)))
                self.player.walking = 'backward'
            else:
                self.player.walking = False
        
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

        self.screen.drawBG()

        if config.FullScreenSweep:
            rays = self.rayCaster.RaySweep(self.player.position,self.player.direction, simplify=True)
        else:
            rays = self.rayCaster.RaySearch(self.player.position,self.player.direction, simplify=True)

        polygons = self.rayCaster.RenderSweep(rays, sort=True)

        sprites = generateSpriteList()
        
        if config.texturedWalls == True:
            self.screen.renderTextured(polygons, sprites)
        else:
            self.screen.render(polygons, sprites)

        self.gui.drawHud()

        if config.debugLevel >= 1:
            self.screen.debugFPS(self.fps)
            if config.debugLevel >= 2:
                self.screen.debugCompass(int(VectorOps.angle(VectorOps.rotate(self.player.direction, math.pi/2)) * 180 / math.pi))
                
        self.screen.update()

    def manageSounds(self):
        if self.player.walking != False:
            self.soundManager.startSound(walking=True, walkDelay=(0.75 if self.player.walking == 'forward' else 1))
        else:
            self.soundManager.startSound(walking=False)

        self.soundManager.playSounds()

    def timer(self):
        self.deltaTime = time.perf_counter() - self.loopTime
        self.loopTime = time.perf_counter()
        self.fpsTime += self.loopTime
        if self.fpsTime > 250:
            self.fps = int(1/self.deltaTime)
            print("FPS:", self.fps)
            self.fpsTime = 0

    def on_execute(self):
        
        while( self._running ):
            self.timer()
            for i in self.screen.events():
                self.on_event(i)
            self.loop()
            self.on_render()
            self.manageSounds()

def mainLaunch(renderer = ''):
    controller = Game()
    controller.on_execute()

if __name__ == "__main__":
    mainLaunch()