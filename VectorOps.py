import math

def sub(minuend, subtrahend):
    if type(minuend[0]) == list: 
        return [[j - k for j,k in zip(i, subtrahend)] for i in minuend]
    else:
        return [j - k for j,k in zip(minuend, subtrahend)]

def add(addend1, addend2):
    if type(addend2) == list: 
        return [j + k for j,k in zip(addend1, addend2)]
    else:
        return [j + addend2 for j in addend1]

def addNormal(addend1, addend2):
    if type(addend2) == list: 
        return normalize([j + k for j,k in zip(addend1, addend2)])
    else:
        return normalize([j + addend2 for j in addend1])

def divide(dividend, divisor):
    if type(divisor) == list: 
        return [j / k for j,k in zip(dividend, divisor)]
    else:
        return [j / divisor if divisor != 0 else 999 for j in dividend]

def multiply(factor1, factor2):
    if type(factor2) == list: 
        return [j * k for j,k in zip(factor1, factor2)]
    else:
        return [j * factor2 for j in factor1]

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

def angVec(ang):
    return [math.sin(ang), math.cos(ang)]

def normalize(vector):
    return [i / length(vector) for i in vector]

def length(vector):
    return sum([i**2 for i in vector])**(1/2)

def difLen(vector1, vector2):
    return length(sub(vector2,vector1))

def difLenNormal(vector1, vector2):
    return length(sub(normalize(vector2),normalize(vector1)))

def distance(vector1, vector2):
    return ((vector1[0] - vector2[0])**2 + (vector1[1] - vector2[1])**2)**(1/2)

def rotate(vector, angle):
    return [vector[0] * math.cos(-angle) - vector[1] * math.sin(-angle), vector[0] * math.sin(-angle) + vector[1] * math.cos(-angle)]

def shift(vector, magnitude, angle1):
    if type(angle1) == list:
        angle1 = angle(angle1)
    return [vector[0] + magnitude * math.sin(angle1), vector[1] + magnitude * math.cos(angle1)]

def vLerp(vector1, vector2, steps):
    steps += 1
    ang = abs(angle(vector1) - angle(vector2))
    dang = (ang if ang <= math.pi else (2 * math.pi) - ang) / steps
    vecs = [vector1]
    ang = 0
    for i in range(steps):
        ang += dang
        vecs.append(rotate(vector1,ang))
    return vecs

def perpendicular(vector, point, magnitude):
    if type(vector) == list or type(vector) == tuple:
        perp = angle((vector[1], -vector[0]))
    else:
        perp = vector + math.pi/2
    return ([i + rotate((0,magnitude), perp)[j] for j, i in enumerate(point)],[i - rotate((0,magnitude), perp)[j] for j, i in enumerate(point)])

def pointPerpendicular(point1, point2, magnitude):
    perp = angle([j-i for i,j in zip(point1, point2)]) + math.pi/2
    return ([i + rotate((0,magnitude), perp)[j] for j, i in enumerate(point2)],point2,[i - rotate((0,magnitude), perp)[j] for j, i in enumerate(point2)])

if __name__ == "__main__":
    print(sub([1,1],[2,2]))
    