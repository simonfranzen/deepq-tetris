colorcodes = {
    'black':30,
    'red':31,
    'green':32,
    'yellow':33,
    'blue':34,
    'purple':35,
    'cyan':36,
    'white':37}

blockcolors = {
    0:'black',
    1:'red',
    2:'green',
    3:'yellow',
    4:'blue',
    5:'purple',
    6:'cyan',
    7:'white'}

def color(s, c):
    return '\033[1;{};40m{}\033[0m'.format(colorcodes[c.lower()],s)
