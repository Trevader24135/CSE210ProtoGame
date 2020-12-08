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

width = 640
height = 480
hudHeight = 75

FOV = (config.FOV * math.pi) / 180
cameraDist = 0.1 / math.tan(FOV / 2)

class Game:
    def __init__(self):
        self.screen = Renderer.pgRenderer(width, height, cameraDist=cameraDist, FogofWar=config.FogofWar, hudHeight=hudHeight)
        
        self._running = True
        self.keysPressed, self.keysHeld = [], []
        self.rayCaster = RayCaster.Screen(mapTools.map, width = width, height = height - hudHeight, supersampling = config.supersampling, cameraDist = cameraDist, Renderer=self.screen)
        self.loopTime, self.fpsTime, self.fps, self.deltaTime = 0, 0, 0, 0
        self.player = entities.Player(position = [2.5,5.5], direction=(1,0))

        self.spritesOnScreen = []
        self.mobAI = entities.MobAI(mapTools.map) #initialize the AI pather with the map data
        self.enemies = [
            entities.Goblin(position = [2.8,1.4]), 

            entities.Goblin(position = [2,8.4]),

            entities.Goblin(position = [7.5,9.5]), 
            
            entities.Goblin(position = [8.5,1.5]), 
            entities.Goblin(position = [7.7,2.3]),
            entities.Goblin(position = [9,3.1]),

            entities.Goblin(position = [12,5.5])
        ]
        for i in self.enemies:
            i.entityList = self.enemies
        
        self.gui = GUI.Hud(self.screen, self.player)

        self.soundManager = SoundEngine.SoundManager()
        self.player.walking = False
        
    def on_event(self, event):
        if event[0] == 'QUIT':
            self._running = False
        elif event[1] == 'press' and not event[0] in self.keysHeld:
            self.keysPressed.append(event[0])
            self.keysHeld.append(event[0])
        elif event[1] == 'release' and event[0] in self.keysHeld:
            self.keysHeld.remove(event[0])
    
    def loop(self):
        def playerMovement():
            if 'left' in self.keysHeld or 'a' in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, -3.14 * self.deltaTime)
            elif 'right' in self.keysHeld or 'd' in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, 3.14 * self.deltaTime)
            if 'up' in self.keysHeld or 'w' in self.keysHeld:
                self.player.move(VectorOps.rotate((0,self.player.maxSpeed * self.deltaTime),VectorOps.angle(self.player.direction)))
                self.player.walking = 'forward'
            elif 'down' in self.keysHeld or 's' in self.keysHeld:
                self.player.move(VectorOps.rotate((0,-self.player.maxSpeed * self.deltaTime * 0.5),VectorOps.angle(self.player.direction)))
                self.player.walking = 'backward'
            else:
                self.player.walking = False
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
        def checkwin():
            if mapTools.map[int(self.player.position[0])][int(self.player.position[1])] == 1:
                print("you win!")
        
        playerMovement()
        checkwin()
        self.spritesOnScreen = generateSpriteList()

        if 'space' in self.keysPressed and len(self.spritesOnScreen) != 0:
            if self.loopTime - self.player.attackCoolDown > self.player.attackTime:
                self.player.attack(self.spritesOnScreen[0][0])

        for enemy in self.enemies: #enemy pathing
            if self.rayCaster.TestLoS(self.player.position, enemy.position):
                if -0.4 < enemy.position[0] - self.player.position[0] < 0.4 and -0.4 < enemy.position[1] - self.player.position[1] < 0.4:
                    continue
                enemy.destination = (self.player.position[0],self.player.position[1])
                try: #throws an error when the enemy is in the same tile as the target
                    path = self.mobAI.findPath( (enemy.position[0],enemy.position[1]), enemy.destination)
                    sConst = enemy.maxSpeed * self.deltaTime
                    enemy.move(VectorOps.multiply(VectorOps.normalize([(path[1][0] - enemy.position[0]), (path[1][1] - enemy.position[1])]),sConst), normalizeResult=False, smoothCollision = True)
                except:
                    pass
        
    def on_render(self):
        self.screen.drawBG()

        if config.FullScreenSweep:
            rays = self.rayCaster.RaySweep(self.player.position,self.player.direction, simplify=True)
        else:
            rays = self.rayCaster.RaySearch(self.player.position,self.player.direction, simplify=True)

        polygons = self.rayCaster.RenderSweep(rays, sort=True)
        
        for enemy in self.enemies: #reset enemy color overlays
            if enemy.colorAniTime - self.loopTime < 0:
                enemy.colorMultiplier = [1,1,1]
        sprites = self.spritesOnScreen[:]
        
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
            self.soundManager.startSound(walking=True, walkDelay=(0.6 if self.player.walking == 'forward' else 1))
        else:
            self.soundManager.startSound(walking=False)

        self.soundManager.playSounds()

    def timer(self):
        self.deltaTime = time.perf_counter() - self.loopTime
        self.loopTime = time.perf_counter()
        self.fpsTime += self.loopTime
        if self.fpsTime > 250:
            self.fps = int(1/self.deltaTime)
            #print("FPS:", self.fps)
            self.fpsTime = 0

    def on_execute(self):
        
        while( self._running ):
            self.timer()
            self.keysPressed = []
            for event in self.screen.events():
                self.on_event(event)
            self.loop()
            self.on_render()
            self.manageSounds()

def mainLaunch(renderer = ''):
    controller = Game()
    controller.on_execute()

if __name__ == "__main__":
    mainLaunch()