import config

import pygame
import pygame.gfxdraw

if config.debugLevel >= 1:
    import DataOps
    pygame.font.init()
    myfont = pygame.font.SysFont('Lucida Console', 10)

goblinSprite = pygame.image.load("assets\\goblin.png")

class pgRenderer:
    def __init__(self, width, height, hudHeight):
        pygame.init()
        self.size = self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.SCALED) # | pygame.FULLSCREEN
        
        self.hudHeight = hudHeight
        
        global hud
        hud = pygame.image.load("assets\\hud.png")
        hud = pygame.transform.scale(hud, (self.width, hud.get_height()))
    
    def drawBG(self):
        self.screen.fill((0,0,0))
        self.screen.fill((92,92,92), (0,int((self.height - self.hudHeight)/2), self.width, int((self.height - self.hudHeight)/2)))

    def drawSprite(self, sprite, corners, distance):
        image = pygame.transform.scale(sprite, (corners[2], corners[3])).convert_alpha()
        color = [int(255 / distance) if 255 / distance > 0 and distance > 1 else 255 if distance <= 1 else 0 for n in [0,1,2]]
        image.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        
        self.screen.blit(image, (corners[0], corners[1] ))
    
    def debugSprites(self, corner):
        pygame.draw.circle(self.screen, 'blue', [corner[0] + (corner[2])/2,10], 5)

    def debugRays(self, rays, color = 'green', length = 10):
        for j,i in enumerate(rays):
            pygame.draw.rect(self.screen, color, [int(DataOps.map(rays[j][5][0], rays[0][5][0], -rays[0][5][0], 0, 640)),0,1,length])

    def debugFPS(self, fps):
        text = myfont.render(str(fps), False, 'white')
        self.screen.blit(text, (self.width - 18,0))

    def debugCompass(self, angle):
        text = myfont.render(str(angle), False, 'white')
        self.screen.blit(text, ((self.width - 36)/2,25))

    def drawWall(self, color, corners, distance):
        pygame.draw.polygon(self.screen, [(int(n / (distance+1)) if n / distance > 0 else 0) for n in color],  corners, 1 if config.debugLevel >= 2 else 0)

    def drawHud(self):
        self.screen.blit(hud, (0, self.height - self.hudHeight))

    def update(self, rect = [0,0,0,0]):
        if rect == [0,0,0,0]:
            rect[2],rect[3] = self.width, self.height
        pygame.display.update(rect)
    
    def events(self):
        keys = []
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                keys.append(['QUIT','QUIT'])
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    keys.append(['QUIT','QUIT'])
                keys.append([pygame.key.name(event.key), 'press'])
            elif event.type == pygame.KEYUP:
                keys.append([pygame.key.name(event.key), 'release'])
        return keys