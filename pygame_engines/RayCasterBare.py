import math

import VectorOps

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

def sortbyindex(List, index):
    sorter = [j for j,i in enumerate(List)]
    sorter.sort(key = [i[index] for i in List].__getitem__)
    temp = List[:]
    for i, j in enumerate(sorter):
        List[i] = temp[j]
    return List

class Screen:
    class Ray:
        def __init__(self, position, direction, angle): #origin of ray, forward direction of player (for non-euclidean distance), angle of ray
            self.directionOriginal = direction
            self.direction = VectorOps.normalize(VectorOps.rotate(direction,angle))
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
                self.position,
                [int((i if j > 0 else i - 0.001 if i - 0.001 >= 0 else 0)) for i,j in zip(self.position, self.direction)],
                ['N' if (fpart(self.position[1]) < 0.001 or fpart(self.position[1]) > 0.999) and self.direction[1] > 0 else
                 'S' if (fpart(self.position[1]) < 0.001 or fpart(self.position[1]) > 0.999) and self.direction[1] <= 0 else
                 'E' if (fpart(self.position[0]) < 0.001 or fpart(self.position[0]) > 0.999) and self.direction[0] > 0 else
                 'W' if (fpart(self.position[0]) < 0.001 or fpart(self.position[0]) > 0.999) and self.direction[0] <= 0 else 'O']]

        def Cast(self):
            try:
                ni = self.NextIntercept()
                while map[ni[3][0]][ni[3][1]] <= 0:
                    ni = self.NextIntercept()
            except:
                pass
            return ni

    def __init__(self, mapData, width = 800, height = 600, cameraDist = 0.1, supersampling = 1, debug = False):
        global map
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
            rays.append(self.Ray(position, i, VectorOps.angle(direction)).Cast())
        return rays

    def RenderSweep(self, rays, sort = False):
        polygons = []
        i = 0
        while i < len(rays):
            try:
                iOne = i
                rectHeightOne = (self.height / 4)/(rays[iOne][0])
                try:
                    while rays[i][4] == rays[i + 1][4] and -0.25 < rays[i][0] - rays[i+1][0] < 0.25 and rays[i][3] == rays[i + 1][3]:
                        i += 1
                except:
                    pass
                
                try:
                    if -0.5 < rays[i][0] - rays[i+1][0] < 0.5:
                        rectHeightTwo = (self.height / 4)/(rays[i+1][0])
                    else:
                        rectHeightTwo = (self.height / 4)/(rays[i][0])
                except:
                    rectHeightTwo = (self.height / 4)/(rays[i][0])

                corners = [[iOne * self.supersampling, int(self.height/2 + rectHeightOne)],
                    [(i+1) * self.supersampling, int(self.height/2 + rectHeightTwo)],
                    [(i+1) * self.supersampling, int(self.height/2 - rectHeightTwo)],
                    [iOne * self.supersampling, int(self.height/2 - rectHeightOne)]]
                
                polygons.append([(rays[iOne][1] if (rays[iOne][1] > rays[i][1]) else rays[i][1]), corners, (rays[i][3][0],rays[i][3][1]), rays[i][4]])
            except:
                pass
            i += 1
        if sort:
            polygons = sortbyindex(polygons, 0)
        return polygons

    def TestLoS(self, positionOne, positionTwo):
        direction = [j - i for i,j in zip(positionOne,positionTwo)]
        if sum(direction) == 0:
            return True
        testerRay = self.Ray(positionOne, direction, 0).Cast()
        directionTwo = [j - i for i,j in zip(positionTwo,testerRay[2])]
        return (True if -0.001 < VectorOps.angle(directionTwo) - VectorOps.angle(direction) < 0.001 else False)

if __name__ == "__main__":
    import os
    from sys import path
    path.append(os.path.abspath(os.getcwd()))
    import protogameBare
    protogameBare.mainLaunch('BARE')