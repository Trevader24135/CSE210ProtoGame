import sys
sys.path.append('pygame_engines')
import config

#West, South, East, North
gw = [[109,109,109],[109,109,109],[109,109,109],[109,109,109],0]
ch = [[110,109,109],[110,109,109],[110,109,109],[110,109,109],0]
rb = [[255,0,0],[0,255,0],[255,255,255],[0,0,255],0]
gray = [[122,122,122],[122,122,122],[122,122,122],[122,122,122],0]
ex = [[109,109,109],[110,110,110],[109,109,109],[109,109,109],255]
tc = [[110,110,109],[110,110,109],[110,110,109],[110,110,109],128]
tcs = [[109,109,109],[110,110,109],[109,109,109],[109,109,109],255]
testmap = [
    [gw, gw, gw, gw, gw, gw, gw],
    [gw, 0, gw, 0, 0, 0, gw], 
    [gw, 0, gw, 0, rb, 0, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [ch, 0, 0, 0, 0, 0, gw], 
    [gw, gw, gw, 0, 0, 0, gw], 
    [gw, gw, gw, gw, 0, gw, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gw, gw, gw, gw, 0, gw, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gw, 0, 0, 0, -1, 0, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gw, gw, gw, gw, gw, gw, gw]]

map = [
   #0  1   2   3   4   5   6   7   8   9   10
    [gw, gw, gw, gw, ch, ch, ch, gw, ch, ch, gw], #0
    [ch, 0 , 0 , gw, 0 , 0 , 0 , gw, 0 , 0 , gw], #1
    [ch, 0 , 0 , gw, 0 , 0 , 0 , gw, 0 , 0 , gw], #2
    [ch, 0 , 0 , gw, 0 , 0 , 0 , gw, gw, 0 , gw], #3
    [gw, gw, 0 , gw, gw, 0 , gw, gw, gw, 0 , gw], #4
    [gw, gw, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , gw], #5
    [gw, gw, gw, gw, gw, gw, gw, gw, 0 , gw, gw], #6
    [ch, 0 , 0 , 0 , gw, 0 , gw, 0 , 0 , 0 , gw], #7
    [ch, 0 , 0 , 0 , 0 , 0 , 0 , 0 , gw, gw, gw], #8
    [ch, 0 , 0 , 0 , gw, gw, gw, 0 , 0 , 0 , gw], #9
    [gw, gw, 0 , gw, gw, ex, gw, gw, 0 , gw, gw], #10
    [gw, 0 , 0 , gw,tcs, 1 ,tcs, gw, 0 , 0 , ch], #11
    [gw, 0 , 0 , gw, 0 , 0 , 0 , gw, 0 , 0 , ch], #12
    [gw, 0 , gw, gw, 0 , 0 , 0 , gw, 0 , 0 , ch], #13
    [gw, 0 , 0 , gw, 0 , gw, gw, gw, gw, 0 , gw], #14
    [gw, 0 , 0 , gw, 0 , gw, 0 , 0 , gw, 0 , gw], #15
    [gw, 0 , 0 , gw, 0 , 0  ,0 , 0 , gw, 0 , gw], #16
    [gw, 0 , gw, gw, gw, gw ,0 , 0 , gw, 0 , gw], #17
    [gw, 0 , 0 , 0 , 0 , 0  ,0 , 0 , gw, 0 , gw], #18
    [gw, gw, gw, gw, gw, gw ,0 , 0 , 0 , 0 , gw], #19
    [ch, 0 , 0 , 0 , gw, gw ,0 , 0 , gw, 0 , gw], #20
    [ch, 0 , 0 , 0 , 0 , 0  ,0 , 0 , gw, gw, gw], #21
    [gw, ch, ch, gw, gw, gw ,ch, ch, gw, gw, gw] #22
   #0  1   2   3   4   5   6   7   8   9   10
]

lightMap = [[0 if type(k) == int else k[4] if k[4] != 0 else -1 for k in j] for j in map]

for i in range(8):
    lightMapTemp = [[i for i in j] for j in lightMap]
    for ypos, y in enumerate(lightMap):
        for xpos, x in enumerate(y):
            if x != 0 and x!= -1:
                for yo in [-1,0,1]:
                    for xo in [-1,0,1]:
                        if xo + yo == 0 or xo + yo == 2:
                            continue
                        try:
                            if lightMap[ypos + yo][xpos + xo] != -1 and x/4 > lightMap[ypos + yo][xpos + xo]:
                                lightMapTemp[ypos + yo][xpos + xo] = x/2
                        except:
                            pass
    lightMap = lightMapTemp

#for i in lightMap:
#    print(i)

directions = {
    'W':0,
    'N':1,
    'E':2,
    'S':3
}