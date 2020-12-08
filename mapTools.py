import sys
sys.path.append('pygame_engines')
import config

#West, South, East, North
gw = [[109,109,109],[109,109,109],[109,109,109],[109,109,109]]
gwchr = [[110,109,109],[110,109,109],[110,109,109],[110,109,109]]
rb = [[255,0,0],[0,255,0],[255,255,255],[0,0,255]]
gray = [[122,122,122],[122,122,122],[122,122,122],[122,122,122]]

testmap = [
    [gw, gw, gw, gw, gw, gw, gw],
    [gw, 0, gw, 0, 0, 0, gw], 
    [gw, 0, gw, 0, rb, 0, gw], 
    [gw, 0, 0, 0, 0, 0, gw], 
    [gwchr, 0, 0, 0, 0, 0, gw], 
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
    [gw, gw, gw, gw, gw, gw, gw, gw, gw, gw, gw], #0
    [gw, 0 , 0 , gw, 0 , 0 , 0 , gw, 0 , 0 , gw], #1
    [gw, 0 , 0 , gw, 0 , 0 , 0 , gw, 0 , 0 , gw], #2
    [gw, 0 , 0 , gw, 0 , 0 , 0 , gw, gw, 0 , gw], #3
    [gw, gw, 0 , gw, gw, 0 , gw, gw, gw, 0 , gw], #4
    [gw, gw, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , gw], #5
    [gw, gw, gw, gw, gw, 0 , gw, gw, 0 , gw, gw], #6
    [gw, 0 , 0 , 0 , gw, 0 , gw, 0 , 0 , 0 , gw], #7
    [gw, 0 , 0 , 0 , 0 , 0 , gw, 0 , gw, gw, gw], #8
    [gw, 0 , 0 , 0 , gw, gw, gw, 0 , 0 , 0 , gw], #9
    [gw, gw, 0 , gw, gw, 1 , gw, gw, 0 , gw, gw], #10
    [gw, gw, 0 , gw, 0 , 0 , 0 , gw, 0 , 0 , gw], #11
    [gw, gw, 0 , 0 , 0 , 0 , 0 , gw, 0 , 0 , gw], #12
    [gw, gw, gw, gw, gw, gw, gw, gw, gw, gw, gw], #13
]
directions = {
    'S':0,
    'W':1,
    'N':2,
    'E':3
}