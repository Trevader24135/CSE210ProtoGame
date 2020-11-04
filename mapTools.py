import sys
sys.path.append('pygame_engines')
import config

#West, South, East, North
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

directions = {
    'S':0,
    'W':1,
    'N':2,
    'E':3
}