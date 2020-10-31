import config
import math

import VectorOps
import ListOps
import DataOps

PreSweepSubdivisions = 2

class Screen:
    class Ray:
        def __init__(self, position, direction, angle, cameraDist): #origin of ray, forward direction of player (for non-euclidean distance), angle of ray
            self.cameraDist = cameraDist
            self.directionOriginal = VectorOps.divide(direction,(direction[1] / self.cameraDist))
            self.direction = VectorOps.normalize(VectorOps.rotate(direction,angle))
            self.position = position[:]
            self.positionOriginal = position[:]
        
        def NextIntercept(self):
            fparts = DataOps.fparta(self.position)
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
                self.position,
                [int((i if j > 0 else i - 0.001 if i - 0.001 >= 0 else 0)) for i,j in zip(self.position, self.direction)],
                ['N' if (DataOps.fpart(self.position[1]) < 0.000000001 or DataOps.fpart(self.position[1]) > 0.999999999) and self.direction[1] > 0 else
                 'S' if (DataOps.fpart(self.position[1]) < 0.000000001 or DataOps.fpart(self.position[1]) > 0.999999999) and self.direction[1] <= 0 else
                 'E' if (DataOps.fpart(self.position[0]) < 0.000000001 or DataOps.fpart(self.position[0]) > 0.999999999) and self.direction[0] > 0 else
                 'W' if (DataOps.fpart(self.position[0]) < 0.000000001 or DataOps.fpart(self.position[0]) > 0.999999999) and self.direction[0] <= 0 else 'O'],
                 self.directionOriginal]

        def Cast(self): #CAST RETURNS [0:Distance, 1:EuclidDistance, 2:endPosition, 3:endTile, 4:tileSide, 5:originalDirection]
            ni = self.NextIntercept()
            while map[ni[3][0]][ni[3][1]] <= 0:
                ni = self.NextIntercept()
            return ni

    def __init__(self, mapData, width = 640, height = 480, cameraDist = 0.1, supersampling = 1, debug = False):
        global map
        map = mapData
        self.width = width
        self.height = height
        self.cameraDist = cameraDist
        self.supersampling = supersampling
        self.debug = debug
    
    def RaySweep(self, position, direction, simplify = False, Renderer = None):
        direction = VectorOps.angle(direction)
        rayscast = 0
        rays = []
        
        if simplify:
            preSweep = [self.Ray(position, VectorOps.normalize([i,self.cameraDist]), direction, self.cameraDist).Cast() for i in [-0.1,0.1]]
            rayscast += len(preSweep)
            i = 0
            while i < len(preSweep) - 1:
                if (preSweep[i][3] != preSweep[i+1][3] or preSweep[i][4] != preSweep[i+1][4]) and VectorOps.difLen(preSweep[i][5], preSweep[i+1][5]) > 0.00025: #there is a change between these two rays
                    preSweep.insert(i+1, self.Ray(position, VectorOps.add(preSweep[i][5],preSweep[i+1][5]), direction, self.cameraDist).Cast() )
                    #for j,k in enumerate(VectorOps.vLerp(preSweep[i][5], preSweep[i+1][5], PreSweepSubdivisions)[1:PreSweepSubdivisions+1]):
                    #    preSweep.insert(i+j+1, self.Ray(position, k, direction, self.cameraDist).Cast() )
                    rayscast += 1
                else:
                    i += 1
            if config.debugLevel >= 1 and Renderer != None:
                Renderer.debugRays(preSweep)

            rays.append(preSweep.pop(0))
            last = rays[-1]
            while len(preSweep) > 1:
                if rays[-1][4] == preSweep[0][4] and rays[-1][3] == preSweep[0][3]:
                    if not ((-1 <= last[3][0] - preSweep[1][3][0] <= 1 and last[3][1] == preSweep[1][3][1]) or (-1 <= last[3][1] - preSweep[1][3][1] <= 1 and last[3][0] == preSweep[1][3][0]) or (-0.7 <= last[0] - preSweep[1][0] <= 0.7)):
                        edge = preSweep.pop(0)
                        edge[5] = preSweep[0][5]
                        rays.append(edge)
                        last = rays[-1]
                    else:
                        last = preSweep.pop(0)
                else:
                    rays.append(preSweep.pop(0))
                    last = rays[-1]
            if len(preSweep) > 0:
                rays.append(preSweep.pop(0))

            if config.debugLevel >= 1 and Renderer != None:
                Renderer.debugRays(rays, color='red', length=20)
        else:
            columns = [[i,self.cameraDist] for i in ListOps.lerp((-0.10, 0.10),int(self.width / self.supersampling))]
            for angle in columns:
                rays.append(self.Ray(position, angle, direction, self.cameraDist).Cast())
                rayscast += 1
            if config.debugLevel >= 1 and Renderer != None:
                Renderer.debugRays(rays)
        #print("rays:",rayscast,len(rays))
        return rays

    def RenderSweep(self, rays, sort = False):
        polygons = []
        i = 0
        lastWasException = False
        while i < len(rays):
            try:
                if rays[i][5] == rays[i+1][5]:
                    i += 1
                    continue
                rectHeightOne = (self.height / 4)/(rays[i][0])

                if i < len(rays):
                    close = (-1 <= rays[i][3][0] - rays[i+1][3][0] <= 1 and -1 <= rays[i][3][1] - rays[i+1][3][1] <= 1)
                    if close: #if they're the same block or close, connect the edges
                        rectHeightTwo = (self.height / 4)/(rays[i+1][0])
                        lastWasException = False
                    elif not lastWasException: #left edge is closer, follow left slope
                        rectHeightTwo = rectHeightOne - ((self.height / 4)/(rays[i-1][0]) - rectHeightOne)
                        lastWasException = True
                    else:
                        rectHeightTwo = (self.height / 4)/(rays[i][0])
                        lastWasException = False
                else:
                    rectHeightTwo = rectHeightOne - ((self.height / 4)/(rays[i-1][0]) - rectHeightOne) #right edge of screen, follow previous slope to approximate out-of-range value
                rectHeightTwo = (self.height / 4)/(rays[i+1][0])
                corners = [
                    [int(DataOps.map(rays[i][5][0], rays[0][5][0], -rays[0][5][0], 0, 640)), int(self.height/2 + rectHeightOne)],
                    [int(DataOps.map(rays[i+1][5][0], rays[0][5][0], -rays[0][5][0], 0, 640)), int(self.height/2 + rectHeightTwo)],
                    [int(DataOps.map(rays[i+1][5][0], rays[0][5][0], -rays[0][5][0], 0, 640)), int(self.height/2 - rectHeightTwo)],
                    [int(DataOps.map(rays[i][5][0], rays[0][5][0], -rays[0][5][0], 0, 640)), int(self.height/2 - rectHeightOne)]
                ]

                polygons.append([(rays[i][1] if (rays[i][1] > rays[i+1][1]) else rays[i+1][1]), corners, (rays[i][3][0],rays[i][3][1]), rays[i][4]])
            except:
                pass
            i += 1
        if sort:
            polygons = ListOps.sortbyindex(polygons, 0)
        return polygons

    def TestLoS(self, positionOne, positionTwo):
        direction = [j - i for i,j in zip(positionOne,positionTwo)]
        if sum(direction) == 0:
            return True
        testerRay = self.Ray(positionOne, direction, 0, self.cameraDist).Cast()
        directionTwo = [j - i for i,j in zip(positionTwo,testerRay[2])]
        return (True if -0.001 < VectorOps.angle(directionTwo) - VectorOps.angle(direction) < 0.001 else False)
