from referee.game import _ADJACENT_STEPS

# Game-algorithm-specific constants:
"""
A border post is a corner of enemy destination.
_BORDER_POST is a dictionary of all four of
these posts for each color.
"""
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
    How many pieces of ours are at border posts.
    """
    output = 0

    for location in _BORDER_POST[colour]:
        if location in state.keys() and state[location] == colour:
            output += 1

    return output

def f2(colour, state):
    """
    How many pieces of ours are at edges.
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
    """
    Match all border posts with our pieces and
    find four pieces that are cloest to border posts.
    """
    return - 1

def f4(colour, state):
    """
    How many pieces of ours will be eaten.
    """

    direction_list = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]
    player_pieces = []
    output = 0

    for k, v in state.items():
        if v == colour:
            player_pieces.append(k)

    for pq, pr in player_pieces:
        for dq, dr in direction_list:
            if (pq+dq, pr+dr) in state:
                if (pq-dq, pr-dr) not in state:
                    output += 1

    return output

def f5(colour, state):
    """
    Find the piece difference between us and enemies.
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
    Find sum of distances between pieces that are closest
    to destination and the destination.
    Only triggers when all enemies are down.
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

    # If enemies are still alive, we hold our positions instead.
    if red != 0 and green != 0 and blue != 0:
        output = 0

    return output

def hex_distance(location1, location2):
    q1 = location1[0]
    q2 = location2[0]
    r1 = location1[1]
    r2 = location2[1]
    output = abs(q1-q1) + abs(r1-r2+q1-q2)
    return output
