import config

import math
import pygame
import time
import mapTools

pygame.init()

import DataOps
pygame.font.init()
myfont = pygame.font.SysFont('Lucida Console', 10)

if config.texturedWalls:
    import DataOps
    import VectorOps
    import ListOps
    MissingTexture = pygame.image.load("assets\\Walls\\MissingTexture2.png")

    colorToTexture = {
        "25500":pygame.image.load("assets\\Walls\\red.png"),
        "02550":pygame.image.load("assets\\Walls\\green.png"),
        "00255":pygame.image.load("assets\\Walls\\blue.png"),
        "000":pygame.image.load("assets\\Walls\\black.png"),
        "255255255":pygame.image.load("assets\\Walls\\white.png"),
        "109109109":pygame.image.load("assets\\Walls\\Wall32T.png"),
        "110109109":pygame.image.load("assets\\Walls\\Wall32TRustedChains.png"),
        "110110109":pygame.image.load("assets\\Walls\\Wall32TTorch.png"),
        "110110110":pygame.image.load("assets\\Walls\\Wall32TExit.png")
    }

armoredGoblinSprite = pygame.image.load("assets\\Mobs\\armoredGoblin.png")
fastGoblinSprite = pygame.image.load("assets\\Mobs\\fastGoblin.png")
goblinSprite = pygame.image.load("assets\\Mobs\\goblin.png")
swordSprite = pygame.image.load("assets\\HUD\\swordFullDiag.png")
swordSprite = pygame.transform.scale(swordSprite, (256, 256))

class pgRenderer:
    def __init__(self, width, height, cameraDist = 0.1, hudHeight = 100, FogofWar=5):
        self.size = self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.SCALED) # | pygame.FULLSCREEN
        
        self.cameraDist = cameraDist
        self.hudHeight = hudHeight
        self.viewportMid = (self.height - self.hudHeight) / 2
        self.FogofWar = FogofWar
        
        self.titleScreenImage = pygame.image.load("assets\\HUD\\titleScreen.png")
        self.titleScreenSubTitleImage = pygame.image.load("assets\\HUD\\titleScreenSubTitle.png")
        self.titleScreenTitleImage = pygame.image.load("assets\\HUD\\titleScreenTitle.png")
        self.titleScreenAuthorsImage = pygame.image.load("assets\\HUD\\titleScreenAuthors.png")
        self.titleScreenBeginImage = pygame.image.load("assets\\HUD\\titleScreenBegin.png")
        self.hud = pygame.image.load("assets\\HUD\\hud.png")
        self.hud = pygame.transform.scale(self.hud, (self.width, self.hudHeight))
        self.winMsg = pygame.image.load("assets\\HUD\\winMsg.png")
        self.deathMsg = pygame.image.load("assets\\HUD\\deathMsg.png")
        self.deltaTime, self.lastTime = 0, time.perf_counter()
        self.weapon = swordSprite
        self.weaponAniTime = 0
        self.weaponPos = [300,150]
        self.weaponAngle = 0

        self.fadeScreen, self.fadeTime, self.fadeDuration, self.fadeHold = None, 0, 0, 0

        self.background = pygame.Surface((self.width,self.height))
        self.background.fill((0,0,0))
        for i in range(0,80):
            pygame.draw.ellipse(self.background, [i,i,i], (-self.width/2, int((self.height - self.hudHeight)/2 + i * 2.5), 2 * self.width, self.height))
        
        self.consoleMessages = ["Welcome to the dungeon adventurer!","Find a way to escape!","W & S to move","A & D to look","Space bar to attack, H to use a health potion"]
    
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

    def drawBG(self):
        self.screen.blit(self.background, (0,0))
        #self.screen.fill((80,80,80), (0,int((self.height - self.hudHeight)/2), self.width, int((self.height - self.hudHeight)/2)))

    def FogofWarColor(self, distance):
        return (255 * (self.FogofWar + 1)**(1/2)) / ( ((self.FogofWar + 1)**(1/2) - 1) * (distance + 1)**(1/2) ) - (255 / ((self.FogofWar + 1)**(1/2) - 1) )

    def drawSprite(self, sprite, corners, distance, colorMultiplier):
        image = pygame.transform.scale(sprite, (corners[2], corners[3])).convert_alpha()
        #color = [int(255 / distance) if 255 / distance > 0 and distance > 1 else 255 if distance <= 1 else 0 for n in [0,1,2]]
        color = self.FogofWarColor(distance)
        color = [int(color * n) if color > 0 and color * n < 255 else 255 if color > 0 else 0 for n in colorMultiplier]
        image.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        
        self.screen.blit(image, (corners[0], corners[1] ))

    def drawSprites(self, sprites, dist = 0):
        for sprite in reversed(sprites):
            if sprite[1] > dist:
                sprites.remove(sprite)
                x = [int((self.cameraDist * math.tan(n) * 10 + 1) * self.width / 2) for n in sprite[2]]
                spriteDist = (sprite[1] - (self.cameraDist / math.cos((sprite[2][0] + sprite[2][1]) / 2))) * math.cos((sprite[2][0] + sprite[2][1]) / 2) #transform to non-euclidean
                spriteHeight = int(((self.viewportMid) * sprite[0].height)/(spriteDist))
                spriteCorners = [x[0], (self.viewportMid) + ((self.height-self.hudHeight) / 4)/(spriteDist) - spriteHeight, x[1] - x[0], int(((self.viewportMid) * sprite[0].height)/(spriteDist))]
                if spriteCorners[2] > self.width:
                    continue

                if config.debugLevel >= 1:
                    self.debugSprites(spriteCorners)
                
                self.drawSprite(sprite[0].sprite, spriteCorners, sprite[1], sprite[0].colorMultiplier)
        return sprites

    def render(self, polygons, sprites):
        for polygon in reversed(polygons):
            sprites = self.drawSprites(sprites, polygon[0])
            pygame.draw.polygon(self.screen, [(int(n - (n * polygon[0]) / (self.FogofWar)) if n - (n * polygon[0]) / (self.FogofWar) > 0 else 0) for n in mapTools.map[polygon[2][0]][polygon[2][1]][mapTools.directions[polygon[3]]] ],  polygon[1], 1 if config.debugLevel >= 2 else 0)
        self.drawSprites(sprites)

    def renderTextured(self, polygons, sprites):
        def getTexture(polygon):
            sprite = colorToTexture.get("".join([str(i) for i in color]), MissingTexture)
            width, height = int(sprite.get_width() / (polygon[0]-2)), int(sprite.get_height() / (polygon[0]-2))
            width, height = width if width > 1 else 2, height if height > 1 else 2
            if polygon[0] > 3:
                sprite = pygame.transform.smoothscale(sprite, (width, height))
            return sprite.convert_alpha()
        def cutTexture(sprite, sides):
            length = VectorOps.distance(sides[0],sides[1])
            width, height = sprite.get_width(), sprite.get_height()
            bigWidth = int(width / length)
            sprite = pygame.transform.scale(sprite, (bigWidth, height))
            chopped = pygame.Surface((width,height))
            #True if right is cut off else false
            side = True if (DataOps.fpart(sides[0][0]) < 0.1 or DataOps.fpart(sides[0][0]) > 0.9) and (DataOps.fpart(sides[0][1]) < 0.1 or DataOps.fpart(sides[0][1]) > 0.9) else False
            
            chopped.blit(sprite, (0,0), (0 if side else bigWidth - width, 0, width, height))
            return chopped.convert_alpha()
        def scaleHeight(px):
            return heightOne * ((wall.get_width() - px) / width) + heightTwo * ((px) / width)
        def darkenSprite(polygon):
            #color = [int(255 / (0.5 + polygon[0])) if 0 < (255 / (0.5 + polygon[0])) < 255 else 0 if (255 / (0.5 + polygon[0])) < 0 else 255 for n in [0,1,2]]
            color = self.FogofWarColor(polygon[0]) + lightValue
            color = [int(color) if 255 > color > 0 else 255 if color > 255 else 0 for n in [0,1,2]]
            sprite.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        def getDimmensions(polygon):
            return (polygon[1][1][0] - polygon[1][0][0]),(polygon[1][0][1] - polygon[1][3][1]),(polygon[1][1][1] - polygon[1][2][1])
        def blitSprite(polygon):
            drawx = 0
            deltax = width / sprite.get_width()
            for i in range(sprite.get_width()):
                try:
                    scaledHeight = int(scaleHeight(drawx)) if polygon[1][0][1] > polygon[1][1][1] else int(scaleHeight(drawx + deltax))
                    scaledSprite = pygame.transform.scale(sprite, (width,scaledHeight + 4))
                    wall.blit(scaledSprite, (int(drawx), (wall.get_height() - scaledHeight - 2)/2), (int(i*deltax),0,deltax + 1,scaledSprite.get_height()))
                except:
                    pass
                drawx += deltax
        def smoothEdges(polygon):
            deltay = polygon[1][0][1] - polygon[1][1][1] if polygon[1][0][1] > polygon[1][1][1] else polygon[1][1][1] - polygon[1][0][1]
            if heightOne > heightTwo:
                pygame.draw.polygon(wall, [0,0,0,0],  [[0,0], [wall.get_width(),0], [wall.get_width(),deltay]], 1 if config.debugLevel >= 2 else 0)
                pygame.draw.polygon(wall, [0,0,0,0],  [[0, wall.get_height()], [wall.get_width(), wall.get_height()], [wall.get_width(),wall.get_height() - deltay]], 1 if config.debugLevel >= 2 else 0)
            else:
                pygame.draw.polygon(wall, [0,0,0,0],  [[0,0], [wall.get_width(),0], [0,deltay]], 1 if config.debugLevel >= 2 else 0)
                pygame.draw.polygon(wall, [0,0,0,0],  [[0, wall.get_height()], [wall.get_width(), wall.get_height()], [0,wall.get_height() - deltay]], 1 if config.debugLevel >= 2 else 0)      
        
        for polygon in reversed(polygons):
            sprites = self.drawSprites(sprites, polygon[0])
            if polygon[0] < self.FogofWar + 3:
                
                color = mapTools.map[polygon[2][0]][polygon[2][1]][mapTools.directions[polygon[3]]]
                lightValue = mapTools.lightMap[polygon[2][0] + (1 if polygon[3] == 'N' else -1 if polygon[3] == 'S' else 0)][polygon[2][1] + (1 if polygon[3] == 'W' else -1 if polygon[3] == 'E' else 0)]

                sprite = getTexture(polygon)

                if not (0.95 < VectorOps.distance(polygon[4][0],polygon[4][1]) < 1.05):
                    sprite = cutTexture(sprite, polygon[4])

                darkenSprite(polygon)
                width, heightOne, heightTwo = getDimmensions(polygon)
                
                wall = pygame.Surface((width,heightOne if heightOne > heightTwo else heightTwo)).convert_alpha()
                wall.fill([0,0,0,0])
                blitSprite(polygon)
                smoothEdges(polygon)
                coords = [polygon[1][0][0], polygon[1][2][1] if polygon[1][2][1] < polygon[1][3][1] else polygon[1][3][1]]
                self.screen.blit(wall, coords)
            else:
                self.render([polygon], [])
        self.drawSprites(sprites)
        
    def drawHud(self, playerInfo = None):
        self.screen.blit(self.hud, (0, self.height - self.hudHeight))
        self.hudConsoleMessages()
        if playerInfo != None:
            text = myfont.render("Hit Points   : {health}".format(health = str(playerInfo.currentHealth)), False, 'white')
            self.screen.blit(text, (320,self.height - self.hudHeight + 5))
            text = myfont.render("Armor        : {defense}".format(defense = str(playerInfo.defense)), False, 'white')
            self.screen.blit(text, (320,self.height - self.hudHeight + 17))
            text = myfont.render("Speed        : {maxSpeed}".format(maxSpeed = str(playerInfo.maxSpeed)), False, 'white')
            self.screen.blit(text, (320,self.height - self.hudHeight + 29))
            text = myfont.render("Attack Damage: {attackDamage} +/- 5".format(attackDamage = str(playerInfo.attackDamage)), False, 'white')
            self.screen.blit(text, (320,self.height - self.hudHeight + 41))
            
            for i, (key, value) in enumerate(playerInfo.inventory.items()):
                text = myfont.render("{Name} : {Quantity}".format(Name=key, Quantity=value), False, 'white')
                self.screen.blit(text, (500, self.height - self.hudHeight + 5 + 12 * i))

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

    def hudConsoleMessages(self):
        for i,message in enumerate(self.consoleMessages):
            text = myfont.render(message, False, 'white')
            self.screen.blit(text, (10,self.height - self.hudHeight + 5 + i*12))
    
    def addConsoleMessage(self, message):
        self.consoleMessages.append(message)
        if len(self.consoleMessages) > 5:
            self.consoleMessages.pop(0)
    
    def drawWeapon(self):
        self.deltaTime = time.perf_counter() - self.lastTime
        self.lastTime = time.perf_counter()

        if time.perf_counter() - self.weaponAniTime > 0.4:
            self.weaponPos = [300,150]
            self.weaponAngle = -30
            self.weapon = pygame.transform.rotate(swordSprite, self.weaponAngle)
        else:
            self.weaponPos = [self.weaponPos[0] + 1 * self.deltaTime, self.weaponPos[1] + 450 * self.deltaTime]
            self.weaponAngle += 360 * self.deltaTime
            self.weapon = pygame.transform.rotate(swordSprite, self.weaponAngle)
        self.screen.blit(self.weapon, self.weaponPos)
    
    def startAttack(self):
        self.weaponPos = [300,150]
        self.weaponAngle = -30
        self.weaponAniTime = time.perf_counter()
    
    def displayGameWin(self):
        self.screen.blit(self.winMsg, ((self.width - self.winMsg.get_width()) / 2, (self.height - self.winMsg.get_height()) / 2))
    
    def displayDeath(self):
        self.screen.blit(self.deathMsg, ((self.width - self.winMsg.get_width()) / 2, (self.height - self.winMsg.get_height()) / 2))

    def titleScreenBegin(self):
        self.screen.blit(self.titleScreenBeginImage, (192,431))
        self.update()

    def fadeOut(self, deltaTime, duration=None, hold=0):
        if duration != None:
            self.fadeHold = hold
            self.fadeScreen = self.screen.convert_alpha()
            self.fadeDuration, self.fadeTime = duration, 0
        
        self.fadeTime += deltaTime
        if not self.fadeTime > self.fadeDuration:
            screen = pygame.Surface(self.size).convert_alpha()
            screen.blit(self.fadeScreen, (0,0))
            color = int((self.fadeTime/self.fadeDuration) * 255)
            color = [255-color for i in [0,1,2]]
            screen.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(screen, (0,0))
            self.update()
        
        if self.fadeTime >= self.fadeDuration + self.fadeHold:
            return False
        return True
    
    def fadeIn(self, deltaTime, duration=None, hold=0, image=None, coords=[0,0]):
        if duration != None:
            self.fadeHold = hold
            self.fadeImage = image
            self.fadeCoords = coords
            self.fadeScreen = self.screen.convert_alpha()
            self.fadeDuration, self.fadeTime = duration, 0
        
        self.fadeTime += deltaTime
        if not self.fadeTime > self.fadeDuration:
            image = pygame.Surface(self.fadeImage.get_size()).convert_alpha()
            image.blit(self.fadeImage, (0,0))
            color = int((self.fadeTime/self.fadeDuration) * 255)
            color = [color for i in [0,1,2]]
            image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(image, self.fadeCoords)
            self.update()
        
        if self.fadeTime >= self.fadeDuration + self.fadeHold:
            return False
        return True

        