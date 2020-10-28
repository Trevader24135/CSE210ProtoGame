#NOTE
#
import sys
sys.path.append('pygame_engines')
import pygame
import math
import time 

import VectorOps
#from skimage import io
#goblin = io.imread("assets\\goblin.png")
goblin = pygame.image.load("assets\\goblin.png")

FOV = 100
width = 800
height = 600
supersampling = 3


FOV *= math.pi / 180
cameraDist = 0.1 / math.tan(FOV / 2)
def genMap():
    def tile(colors):
        colors = [str(n) for n in colors]
        colors = ['00' + n if len(n) == 1 else '0' + n if len(n) == 2 else n for n in colors]
        colors = sum([sum([int(n) << (6 - m*3) for m,n in enumerate(i)]) << (27 - j * 9) for j,i in enumerate(colors)])
        return colors
    #[[Scolor],[Wcolor],[Ncolor],[Ecolor]]
    gw = tile([333,333,333,333])
    rb = tile([700,70,7,707])

    return [
        [gw, gw, gw, gw, gw, gw, gw],
        [gw, 0, gw, 0, 0, 0, gw], 
        [gw, 0, gw, 0, rb, 0, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [rb, 0, 0, 0, 0, 0, gw], 
        [gw, gw, gw, 0, 0, gw, gw], 
        [gw, gw, gw, gw, 0, gw, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [gw, gw, gw, gw, 0, gw, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [gw, 0, 0, 0, -1, 0, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [gw, gw, gw, gw, gw, gw, gw]]#""""
map = genMap()

def numToColor(number, side):
    binstr = {
        '000':0,
        '001':36,
        '010':73,
        '011':109,
        '100':146,
        '101':183,
        '110':219,
        '111':255
    }
    number = bin(number + (1<<36))
    if side == ['W']:
        number = number[3:12]
    elif side == ['N']:
        number = number[12:21]
    elif side == ['E']:
        number = number[21:30]
    elif side == ['S']:
        number = number[30:39]
    color = [binstr[number[0:3]],binstr[number[3:6]],binstr[number[6:9]]]
    return color

class Object:
    def __init__(self, position = [0,0], velocity = [0,0], sprite = "", health = 100, radius = 0.25):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.sprite = sprite
        self.health = health

    def move(self, direction):
        def mapRel(direction):
            return map[int(self.position[0]) + direction[0]][int(self.position[1]) + direction[1]]
        
        def checkCollision(direction): #run 2 checks in each direction, at each side of the player
            
            if direction[0] > 0 and mapRel((1,0)) > 0 and VectorOps.fpart(self.position[0]) > 1 - self.radius:
                direction[0] = 0
            elif direction[0] < 0 and mapRel((-1,0)) > 0 and VectorOps.fpart(self.position[0]) < self.radius:
                direction[0] = 0
            if direction[1] > 0 and mapRel((0,1)) > 0 and VectorOps.fpart(self.position[1]) > 1 - self.radius:
                direction[1] = 0
            elif direction[1] < 0 and mapRel((0,-1)) > 0 and VectorOps.fpart(self.position[1]) < self.radius:
                direction[1] = 0
            return direction
        
        direction = checkCollision(direction)
        self.position = [i + direction[j] for j,i in enumerate(self.position)]

class Player(Object):
    def __init__(self):
        super().__init__(position = [3.5,3.5])
        self.direction = VectorOps.normalize((-1,0))

class Goblin(Object):
    def __init__(self):
        super().__init__(position = [3.1,3.1], sprite = goblin)

class Game:
    def __init__(self):
        pygame.init()
        self._running = True
        self.size = self.width, self.height = width, height
        self.keysHeld = []
        self.screen = pygame.display.set_mode(self.size)
        self.screen.set_alpha(None)
        self.rayCaster = RayCaster.Screen(map, width = width, height = height, supersampling = supersampling, cameraDist = cameraDist, debug = False)
        self.loopTime, self.fpsTime = 0, 0
        self.player = Player()

        self.enemies = []
        self.enemies.append(Goblin())
        
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
            if event.key in self.keysHeld:
                self.keysHeld.remove(event.key)
    
    def loop(self):
        def playerMovement():
            if 276 in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, -3.14 * self.deltaTime)
            elif 275 in self.keysHeld:
                self.player.direction = VectorOps.rotate(self.player.direction, 3.14 * self.deltaTime)
            if 273 in self.keysHeld:
                self.player.move(VectorOps.rotate((0,1.5 * self.deltaTime),VectorOps.angle(self.player.direction)))
            elif 274 in self.keysHeld:
                self.player.move(VectorOps.rotate((0,-1.5 * self.deltaTime),VectorOps.angle(self.player.direction)))
        
        playerMovement()

    def on_render(self):
        def generateSpriteList():
            sprites = []
            for i in self.enemies:
                spriteDist = VectorOps.distance(self.player.position, i.position)
                sprites.append([i, spriteDist])

            for i in sprites:
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
            for i in sprites:
                if i[1] > dist:
                    sprites.remove(i)

                    x = [int((cameraDist * math.tan(n) * 10 + 1) * width / 2) for n in i[2]]
                    if x[1] - x[0] > self.width / 2:
                        continue

                    spriteDist = (i[1] - (cameraDist / math.cos((i[2][0] + i[2][1]) / 2))) * math.cos((i[2][0] + i[2][1]) / 2) #transform to non-euclidean
                    y = int((self.height / 3)/(spriteDist))
                    
                    Sprite = pygame.transform.scale(i[0].sprite, (x[1] - x[0], y)).convert_alpha()
                    color = [int(255 / i[1]) if 255 / i[1] > 0 and i[1] > 1 else 255 if i[1] <= 1 else 0 for n in [0,1,2]]
                    Sprite.fill(color, special_flags=pygame.BLEND_RGB_MULT)
                    self.screen.blit(Sprite, (x[0], (self.height - y)/2  + (self.height / 8)/(spriteDist)))
            return sprites

        self.screen.fill((0,0,0))
        self.screen.fill((92,92,92), (0,int(self.height/2), width, int(self.height/2)))
    
        rays = self.rayCaster.RaySweep(self.player.position,self.player.direction)
        polygons = self.rayCaster.RenderSweep(rays, sort=True)

        sprites = generateSpriteList()

        for i in reversed(polygons):
            sprites = drawSprites(sprites, i[0])
            pygame.draw.polygon(self.screen, [(int(n / i[0]) if n / i[0] > 0 and i[0] > 1 else n if i[0] <= 1 else 0) for n in numToColor(map[i[2][0]][i[2][1]], i[3])], i[1], 0)
        drawSprites(sprites)
        
        pygame.display.update()

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
            for event in pygame.event.get():
                self.on_event(event)
            self.loop()
            self.on_render()

        pygame.quit()

def mainLaunch(renderer = ''):
    global RayCaster
    import RayCasterBare as RayCaster
    controller = Game()
    controller.on_execute()

if __name__ == "__main__":
    mainLaunch()