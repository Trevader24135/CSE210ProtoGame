gw = [[109,109,109],[109,109,109],[109,109,109],[109,109,109]]
gwchr = [[110,109,109],[110,109,109],[110,109,109],[110,109,109]]
rb = [[255,0,0],[0,255,0],[255,255,255],[0,0,255]]
gray = [[122,122,122],[122,122,122],[122,122,122],[122,122,122]]

map = [
    [gw, gw, gw, gw, gw, gw, gw],
    [gw, 0, gw, 0, 0, 0, gw], 
    [gw, 0, gray, 0, rb, 0, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gwchr, 0, 0, 0, 0, 0, gw], 
    [gw, gw, gw, 0, 0, gw, gw], 
    [gw, gw, gw, gw, 0, gw, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gw, gw, gw, gw, 0, gw, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gw, 0, 0, 0, -1, 0, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gw, gw, gw, gw, gw, gw, gw]]

mapEnlargened = []
for y in map:
    row = []
    for x in y:
        if type(x) == int:
            row.append(0)
        else:
            row.append(1)
    mapEnlargened.append(row)

for i in mapEnlargened:
    print(i)