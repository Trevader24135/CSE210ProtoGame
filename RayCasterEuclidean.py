#THIS CAN BE MUCH MORE EFFICIENT. IT CAN STEP BY INDICES INSTEAD OF BY TINY STEPS

import VectorOps

def lerp(endpoints, steps):
    interpolated = [endpoints[0]]
    delta = (endpoints[1] - endpoints[0]) / (steps - 1)
    for i in range(steps - 1):
        interpolated.append(interpolated[i] + delta)
    return interpolated

class Screen:
    class Ray:
        def __init__(self, position, direction, startDist = 0, stepSize = 0.05):
            self.step = stepSize
            self.direction = [i * self.step for i in VectorOps.normalize(direction)]
            self.position = [i + (j * startDist) for i, j in zip(position, direction)]
            self.distance = startDist
        
        def Cast(self):
            try:
                while map[int(self.position[0])][int(self.position[1])] == 0:
                    self.position = [i + self.direction[j] for j,i in enumerate(self.position)]
                    self.distance += self.step
                return self.distance, (int(self.position[0]),int(self.position[1]))
            except:
                pass

    def __init__(self, mapData, width, height, cameraDist = 0.1, supersampling = 1):
        global map
        map = mapData
        self.width = width
        self.height = height
        self.cameraDist = cameraDist
        self.supersampling = supersampling
    
    def RaySweep(self, position, direction, step = 0.05):
        columns = [[i,self.cameraDist] for i in lerp((-0.10, 0.10),int(10))]
        dists = []
        for i in columns:
            dists.append(self.Ray(position, VectorOps.rotate(i, VectorOps.angle(direction)), startDist = 0, stepSize = 0.1).Cast()[0])
        minDist = min(dists) - 0.1

        columns = [VectorOps.normalize([i,self.cameraDist]) for i in lerp((-0.10, 0.10),int(self.width / self.supersampling))]
        rays = []
        for i in columns:
            rays.append(self.Ray(position, VectorOps.rotate(i, VectorOps.angle(direction)), startDist = minDist, stepSize = step).Cast())
        return rays