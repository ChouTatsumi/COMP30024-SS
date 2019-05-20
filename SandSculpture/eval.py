def eval(colour, state):
    w1 = 100
    w2 = -1
    w3 = 3
    w4 = -20
    w5 = 20
    w6 = 30
    return w1 * f1(colour, state) + w2 * f2(colour, state) + \
            w3 * f3(colour, state) + w4 * f4(colour, state) + \
            w5 * f5(colour, state) + w6 * f6(colour, state)

def f1(colour, state):
    """
    The difference of pieces between self and the enemies
    """
    red = 0
    green = 0
    blue = 0
    output = 0

    for v in state.values():
        if v == 'r':
            red += 1
        elif v == 'g':
            green += 1
        elif v == 'b':
            blue += 1
        else:
            print('ERROR input in state')
            exit(-1)

    if colour == 'red':
        output = 2 * red - green - blue
    elif colour == 'green':
        output = 2 * green - red - blue
    elif colour == 'blue':
        output = 2 * blue - red - green
    else:
        print('ERROR input colour')
        exit(-1)

    return output

def f2(colour, state):
    """
    total move from this state to terminal (exit)
    """
    return - 1

def f3(colour, state):
    return - 1

def f4(colour, state):
    return - 1

def f5(colour, state):
    return - 1

def f6(colour, state):
    return - 1
