import math

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