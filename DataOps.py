def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def fpart(number):
  return number - int(number)

def fparta(number):
  return [i - int(i) for i in number]
