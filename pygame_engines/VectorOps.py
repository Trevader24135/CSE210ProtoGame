import math

def sub(minuend, subtrahend):
    if type(minuend[0]) == list: 
        return [[j - k for j,k in zip(i, subtrahend)] for i in minuend]
    else:
        return [j - k for j,k in zip(minuend, subtrahend)]

def swap(vector):
    return [i for i in reversed(vector)]

def angleWrap(angle, ran = [-1,1]):
    ran = [ran[0] * math.pi, ran[1] * math.pi]
    while not (ran[0] < angle < ran[1]):
        if angle < ran[0]:
            angle += 2 *math.pi
        else:
            angle -= 2 *math.pi
    return angle

def fpart(number):
    return number - int(number)
    
def angle(vector):
    if vector[0] == 0:
        return (0 if vector[1] > 0 else math.pi)
    elif vector[1] == 0:
        return (math.pi/2 if vector[0] > 0 else (3 * math.pi) / 2)
    ang = math.atan(abs(vector[0])/abs(vector[1]))
    if vector[1] > 0:
        return (ang if vector[0] > 0 else 2 * math.pi - ang)
    else:
        return math.pi - ang if vector[0] > 0 else math.pi + ang

def length(vector):
    return sum([i**2 for i in vector])**(1/2)

def normalize(vector):
    return [i / length(vector) for i in vector]

def rotate(vector, angle):
    return [vector[0] * math.cos(-angle) - vector[1] * math.sin(-angle), vector[0] * math.sin(-angle) + vector[1] * math.cos(-angle)]

def shift(vector, magnitude, angle1):
    if type(angle1) == list:
        angle1 = angle(angle1)
    return [vector[0] + magnitude * math.sin(angle1), vector[1] + magnitude * math.cos(angle1)]

def distance(vector1, vector2):
    return ((vector1[0] - vector2[0])**2 + (vector1[1] - vector2[1])**2)**(1/2)

def pointPerpendicular(point1, point2, magnitude):
    perp = angle([j-i for i,j in zip(point1, point2)]) + math.pi/2
    return ([i + rotate((0,magnitude), perp)[j] for j, i in enumerate(point2)],point2,[i - rotate((0,magnitude), perp)[j] for j, i in enumerate(point2)])

def perpendicular(vector, point, magnitude):
    if type(vector) == list or type(vector) == tuple:
        perp = angle((vector[1], -vector[0]))
    else:
        perp = vector + math.pi/2
    return ([i + rotate((0,magnitude), perp)[j] for j, i in enumerate(point)],[i - rotate((0,magnitude), perp)[j] for j, i in enumerate(point)])

if __name__ == "__main__":
    pass
    #print(angleWrap(-10))