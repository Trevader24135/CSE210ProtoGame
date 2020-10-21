#NOTE
#
#
#
#

import pygame
import math
import time 

import VectorOps

cameraDist = 0.08
FOV = 90
width = 800
height = 600
supersampling = 5

FOV = (FOV * 180) / math.pi
map = [
    [1,3,1,1,1,1,1],
    [1,0,1,0,0,0,1],
    [1,0,1,0,2,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,1,4,0,0,1,1],
    [1,1,1,1,0,1,1],
    [6,0,0,0,0,0,1],
    [1,1,4,1,0,1,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1],]

class Object:
    def __init__(self, position = [0,0], velocity = [0,0], sprite = "", health = 100):
        self.position = position
        self.velocity = velocity
        self.sprite = sprite
        self.health = health
    
    def move(self, direction):
        self.position = [i + direction[j] for j,i in enumerate(self.position)]

class Player(Object):
    def __init__(self):
        super().__init__(position = [3.5,3.5])
        self.direction = VectorOps.normalize((0,-1))

class Game:
    def __init__(self):
        pygame.init()
        self._running = True
        self.size = self.width, self.height = width, height
        self.keysHeld = []
        self.screen = pygame.display.set_mode(self.size, pygame.HWACCEL | pygame.HWSURFACE | pygame.DOUBLEBUF)# | pygame.FULLSCREEN
        self.screen.set_alpha(None)
        self.rayCaster = RayCaster.Screen(self.screen, map, width = width, height = height, supersampling = supersampling, cameraDist = cameraDist, debug = False)
        self.loopTime = 0
        self.player = Player()
        self.timerFrame, self.timerAverage = 0, 0
        
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27: #escape to quit the game
                self._running = False
            #print("KEYDOWN: " + str(event.key))#276 left 275 right #273 up 274 down
            if not event.key in self.keysHeld:
                self.keysHeld.append(event.key)
        elif event.type == pygame.KEYUP:
            #print("KEYUP: " + str(event.key))
            if event.key in self.keysHeld:
                self.keysHeld.remove(event.key)
    
    def loop(self):
        if 276 in self.keysHeld:
            self.player.direction = VectorOps.rotate(self.player.direction, -3.14 * self.deltaTime)
        elif 275 in self.keysHeld:
            self.player.direction = VectorOps.rotate(self.player.direction, 3.14 * self.deltaTime)
        if 273 in self.keysHeld:
            self.player.move(VectorOps.rotate((0,1.5 * self.deltaTime),VectorOps.angle(self.player.direction)))
        elif 274 in self.keysHeld:
            self.player.move(VectorOps.rotate((0,-1.5 * self.deltaTime),VectorOps.angle(self.player.direction)))

    def on_render(self):
        self.screen.fill((92,92,92))
        pygame.draw.rect(self.screen, (48,48,48), [0,height/2, width, height/2], 0)

        rays = self.rayCaster.RaySweep(self.player.position,self.player.direction)
        self.rayCaster.RenderSweep(rays)

        pygame.display.flip()

    def timer(self):
        self.deltaTime = time.perf_counter() - self.loopTime
        self.loopTime = time.perf_counter()
        if self.timerFrame >= 60:
            print(round((self.timerAverage / 60) * 1000, 2), " ms")
            self.timerFrame, self.timerAverage = 0, 0
        else:
            self.timerAverage += self.deltaTime
        self.timerFrame += 1

    def on_execute(self):
        while( self._running ):
            self.timer()
            for event in pygame.event.get():
                self.on_event(event)
            self.loop()
            self.on_render()

        pygame.quit()

def mainLaunch(renderer = ''):
    global RayCaster
    if renderer == 'EUCLIDEAN':
        import RayCasterEuclidean as RayCaster
    elif renderer == 'NOTEXTURES':
        import RayCasterNoTextures as RayCaster
    elif renderer == 'MANUALTEXTURES':
        import RayCasterManualTextures as RayCaster
    elif renderer == 'GFX':
        import RayCasterGFX as RayCaster
    else:
        import RayCasterNoTextures as RayCaster
    controller = Game()
    controller.on_execute()

if __name__ == "__main__":
    mainLaunch()
