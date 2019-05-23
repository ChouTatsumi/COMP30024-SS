from referee.game import _ADJACENT_STEPS

# Game-algorithm-specific constants:
# 此处用于解释什么是门（敌方终点的角落）
_BORDER_POST = {
    'red': {(0, -3), (3, -3), (3, 0), (0, 3)},
    'green': {(-3, 3), (-3, 0), (3, 0), (0, 3)},
    'blue': {(-3, 3), (-3, 0), (0, -3), (3, -3)},
}

def eval(colour, state):
    w1 = 10
    w2 = 3
    w3 = -1
    w4 = -50
    w5 = 100
    w6 = 5
    return w1 * f1(colour, state) + w2 * f2(colour, state) + \
            w3 * f3(colour, state) + w4 * f4(colour, state) + \
            w5 * f5(colour, state) + w6 * f6(colour, state)

def f1(colour, state):
    """
    有多少我方棋子攻占“下水道”
    """
    output = 0

    for location in _BORDER_POST[colour]:
        if location in state.keys() and state[location] == colour:
            output += 1

    return output

def f2(colour, state):
    """
    有多少我方棋子位处边缘
    """
    output = 0

    for k, v in state.items():
        if v == colour:
            q = k[0]
            r = k[1]
            if abs(q) == 3 or abs(r) == 3 or abs(q + r) == 3:
                output += 1

    return output

def f3(colour, state):
    return - 1

def f4(colour, state):
    return - 1

def f5(colour, state):
    """
    The difference of pieces between self and the enemies
    """
    red = 0
    green = 0
    blue = 0
    output = 0

    for v in state.values():
        if v == 'red':
            red += 1
        elif v == 'green':
            green += 1
        elif v == 'blue':
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

def f6(colour, state):
    """
    total move from this state to terminal (exit)
    prioritise the farest piece
    if there is more than 4 pieces, only the nearest will be considered
    并根据敌方数量调整权重
    """
    red = 0
    green = 0
    blue = 0
    output = 0

    # record all pieces in order to select the min 4 results
    distance = []
    for k, v in state.items():
        if v == 'red':
            if v == colour:
                distance.append(3 - k[0])
            red += 1
        elif v == 'green':
            if v == colour:
                distance.append(3 - k[1])
            green += 1
        elif v == 'blue':
            if v == colour:
                distance.append(3 + k[0] + k[1])
            blue += 1
        else:
            print('ERROR input in state')
            exit(-1)

    output = sum(sorted(distance)[:4])

    # 如果敌方均健在，则不考虑移动至终点，优先守门
    if red != 0 and green != 0 and blue != 0:
        output = 0

    return output
