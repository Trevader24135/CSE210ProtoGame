import sys
sys.path.append('pygame_engines')
import config

def genMap():
    def tile(colors):
        colors = [str(n) for n in colors]
        colors = ['00' + n if len(n) == 1 else '0' + n if len(n) == 2 else n for n in colors]
        colors = sum([sum([int(n) << (6 - m*3) for m,n in enumerate(i)]) << (27 - j * 9) for j,i in enumerate(colors)])
        return colors
    #[[Scolor],[Wcolor],[Ncolor],[Ecolor]]
    gw = tile([333,333,333,333]) # 29451204315
    rb = tile([700,70,7,707])
    
    return [
        [gw, gw, gw, gw, gw, gw, gw],
        [gw, 0, gw, 0, 0, 0, gw], 
        [gw, 0, gw, 0, rb, 0, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [rb, 0, 0, 0, 0, 0, gw], 
        [gw, gw, gw, 0, 0, gw, gw], 
        [gw, gw, gw, gw, 0, gw, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [gw, gw, gw, gw, 0, gw, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [gw, 0, 0, 0, -1, 0, gw], 
        [gw, 0, 0, 0, 0, 0, gw], 
        [gw, gw, gw, gw, gw, gw, gw]]#""""
map = genMap()

def numToColor(number, side):
    binstr = {
        '000':0,
        '001':36,
        '010':73,
        '011':109,
        '100':146,
        '101':183,
        '110':219,
        '111':255
    }
    number = bin(number + (1<<36))
    if side == ['W']:
        number = number[3:12]
    elif side == ['N']:
        number = number[12:21]
    elif side == ['E']:
        number = number[21:30]
    elif side == ['S']:
        number = number[30:39]
    color = [binstr[number[0:3]],binstr[number[3:6]],binstr[number[6:9]]]
    return color
