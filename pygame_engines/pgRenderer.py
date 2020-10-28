import pygame

class pgRenderer:
    def __init__(self, width, height):
        pygame.init()
        self.size = self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.size)
    
    def drawBG(self):
        self.screen.fill((0,0,0))
        self.screen.fill((92,92,92), (0,int(self.height/2), self.width, int(self.height/2)))

    def drawSprite(self, sprite, corners, distance):
        image = pygame.transform.scale(sprite, (corners[2], corners[3])).convert_alpha()
        color = [int(255 / distance) if 255 / distance > 0 and distance > 1 else 255 if distance <= 1 else 0 for n in [0,1,2]]
        image.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        
        self.screen.blit(image, (corners[0], corners[1] ))
    
    def drawWall(self, color, corners, distance):
        pygame.draw.polygon(self.screen, [(int(n / distance) if n / distance > 0 and distance > 1 else n if distance <= 1 else 0) for n in color], corners, 0)

    def update(self):
        pygame.display.update()
    
    def events(self):
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keys.append(['QUIT','QUIT'])
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    keys.append(['QUIT','QUIT'])
                keys.append([event.key, 'press'])
            elif event.type == pygame.KEYUP:
                keys.append([event.key, 'release'])
        return keys