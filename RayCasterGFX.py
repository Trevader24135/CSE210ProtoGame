#THIS CAN BE MUCH MORE EFFICIENT. IT CAN STEP BY INDICES INSTEAD OF BY TINY STEPS
import pygame
import pygame.gfxdraw
import math

import VectorOps
from skimage import io

wall = pygame.image.load("Wall.png")
print(wall)
flatness = 1.2

colors = [
    [255,255,255],
    [255,0,0],
    [255,255,0],
    [0,255,0],
    [0,255,255],
    [0,0,255],
    [255,0,255]]

def lerp(endpoints, steps):
    interpolated = [endpoints[0]]
    delta = (endpoints[1] - endpoints[0]) / (steps - 1)
    for i in range(steps - 1):
        interpolated.append(interpolated[i] + delta)
    return interpolated

def fpart(number):
    return number - int(number)

def fparta(number):
    return [i - int(i) for i in number]

def skew(corners, size, point):
    C1 = (size[0] - point[0]) * (size[1] - point[1])
    C2 = (point[0]) * (size[1] - point[1])
    C3 = (size[0] - point[0]) * (point[1])
    C4 = (point[0]) * (point[1])
    X = ((corners[0][0] * C1) + (corners[1][0] * C2) + (corners[2][0] * C4) + (corners[3][0] * C3)) / (size[0] * size[1])
    Y = ((corners[0][1] * C1) + (corners[1][1] * C2) + (corners[2][1] * C4) + (corners[3][1] * C3)) / (size[0] * size[1])
    return [int(X),int(Y)]

class Screen:
    class Ray:
        def __init__(self, position, direction, angle):
            self.directionOriginal = direction
            self.direction = VectorOps.normalize(VectorOps.rotate(direction,VectorOps.angle(angle)))
            self.position = position[:]
            self.positionOriginal = position[:]
        
        def NextIntercept(self):
            fparts = fparta(self.position)
            if self.direction[0] == 0:
                dx = 999
            else:
                dx = (fparts[0] if self.direction[0] < 0 else 1 - fparts[0])
                dx = (dx if dx != 0 else 1 ) / abs(self.direction[0])
            if self.direction[1] == 0:
                dy = 999
            else:
                dy = (fparts[1] if self.direction[1] < 0 else 1 - fparts[1])
                dy = (dy if dy != 0 else 1 ) / abs(self.direction[1])
            
            if dx <= dy:
                self.position[0] += dx * self.direction[0]
                self.position[1] += dx * self.direction[1]
            else:
                self.position[0] += dy * self.direction[0]
                self.position[1] += dy * self.direction[1]
            distance = ((self.position[0] - self.positionOriginal[0])**2 + (self.position[1] - self.positionOriginal[1])**2)**(1/2)
            distanceNonEuclidean = (distance - VectorOps.length(self.directionOriginal))*math.cos(math.atan(self.directionOriginal[0]/self.directionOriginal[1]))
            return [distanceNonEuclidean,
                distance,
                [int((i if j > 0 else i - 0.001 if i - 0.001 >= 0 else 0)) for i,j in zip(self.position, self.direction)],
                ['N' if (fpart(self.position[1]) < 0.001 or fpart(self.position[1]) > 0.999) and self.direction[1] > 0 else
                 'S' if (fpart(self.position[1]) < 0.001 or fpart(self.position[1]) > 0.999) and self.direction[1] <= 0 else
                 'E' if (fpart(self.position[0]) < 0.001 or fpart(self.position[0]) > 0.999) and self.direction[0] > 0 else
                 'W' if (fpart(self.position[0]) < 0.001 or fpart(self.position[0]) > 0.999) and self.direction[0] <= 0 else 'O']]

        def Cast(self):
            try:
                ni = self.NextIntercept()
                while map[ni[2][0]][ni[2][1]] == 0:
                    ni = self.NextIntercept()
            except:
                pass
            return ni

    def __init__(self, pyGameSurface, mapData, width = 800, height = 600, cameraDist = 0.1, supersampling = 1, debug = False):
        global map
        self.screen = pyGameSurface
        map = mapData
        self.width = width
        self.height = height
        self.cameraDist = cameraDist
        self.supersampling = supersampling
        self.debug = debug
    
    def RaySweep(self, position, direction):
        columns = [[i,self.cameraDist] for i in lerp((-0.10, 0.10),int(self.width / self.supersampling))]
        rays = []
        for i in columns:
            rays.append(self.Ray(position, i, direction).Cast())
        return rays

    def RenderSweep(self, rays):
        i = 0
        while i < len(rays):
            try:
                iOne = i
                rectHeightOne = (self.height / 4)/(rays[iOne][0] * flatness)
                try:
                    while rays[i][3] == rays[i + 1][3] and -0.5 < rays[i][0] - rays[i+1][0] < 0.5 and rays[i][2] == rays[i + 1][2]:
                        i += 1
                except:
                    pass
                rectHeightTwo = (self.height / 4)/(rays[i][0] * flatness)

                corners = [[iOne * self.supersampling, self.height/2 + rectHeightOne],
                    [(i+1) * self.supersampling, self.height/2 + rectHeightTwo],
                    [(i+1) * self.supersampling, self.height/2 - rectHeightTwo],
                    [iOne * self.supersampling, self.height/2 - rectHeightOne]]

                if map[rays[i][2][0]][rays[i][2][1]] != 1:
                    pygame.draw.polygon(self.screen, [(int(n - (rays[i][1] * 30)) if n - (rays[i][1] * 30) > 1 else 1) for n in colors[map[rays[i][2][0]][rays[i][2][1]]]], corners, 2 if self.debug else 0)
                else:
                    pygame.gfxdraw.textured_polygon(self.screen, corners, wall, 0, 0)
            except:
                pass
            i += 1

if __name__ == "__main__":
    import protogame
    protogame.mainLaunch()