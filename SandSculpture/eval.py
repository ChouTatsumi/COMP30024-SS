# Game-algorithm-specific constants:
_ADJACENT_STEPS = [(-1, +0), (+0, -1), (+1, -1), (+1, +0), (+0, +1), (-1, +1)]

"""
A border post is a corner of enemy destination.
_BORDER_POST is a dictionary of all four of
these posts for each color.
"""
_BORDER_POSTS = {
    'red': {(0, -3), (3, -3), (3, 0), (0, 3)},
    'green': {(-3, 3), (-3, 0), (3, 0), (0, 3)},
    'blue': {(-3, 3), (-3, 0), (0, -3), (3, -3)},
}


def eval(colour, state):
    w1 = 10
    w2 = 3
    w3 = -1
    w4 = -100
    w5 = 20
    w6 = 5
    w7 = 300

    return w1 * f1(colour, state) + w2 * f2(colour, state) + \
        w3 * f3(colour, state) + w4 * f4(colour, state) + \
        w5 * f5(colour, state) + w6 * f6(colour, state) + \
        w7 * f7(colour, state)


def f1(colour, state):
    """
    How many pieces of ours are at border posts.
    """
    output = 0

    for location in _BORDER_POSTS[colour]:
        if location in state.keys() and state[location] == colour:
            output += 1

    return output


def f2(colour, state):
    """
    How many pieces of ours are at edges.
    """
    output = 0

    for (q, r), v in state.items():
        if v == colour:
            if abs(q) == 3 or abs(r) == 3 or abs(q + r) == 3:
                output += 1

    return output


def f3(colour, state):
    """
    Match all border posts with our pieces and
    find four pieces that are cloest to border posts.
    """
    output = 0

    player_pieces = []
    for k, v in state:
        if v == colour:
            player_pieces.append(k)

    for post in _BORDER_POSTS[colour]:
        min_idx = 0
        #Any location is less than 7 steps away from any other locations.
        min_distance = 7

        for i in range(len(player_pieces)):
            d = hex_distance(post, player_pieces[i])
            if d < min_distance:
                min_distance = d
                min_idx = i

        if len(player_pieces) > 0:
            output += min_distance
            player_pieces.pop(min_idx)

    return output


def f4(colour, state):
    """
    How many pieces of ours will be eaten.
    """
    player_pieces = []
    output = 0

    for k, v in state.items():
        if v == colour:
            player_pieces.append(k)

    for pq, pr in player_pieces:
        for dq, dr in _ADJACENT_STEPS:
            if (pq + dq, pr + dr) in state:
                opposite = (pq - dq, pr - dr)
                if not (opposite in state or out_of_board(opposite)):
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
    for (q, r), v in state.items():
        if v == 'red':
            if v == colour:
                distance.append(3 - q)
            red += 1
        elif v == 'green':
            if v == colour:
                distance.append(3 - r)
            green += 1
        elif v == 'blue':
            if v == colour:
                distance.append(3 + q + r)
            blue += 1
        else:
            print('ERROR input in state')
            exit(-1)

    output = sum(sorted(distance)[:4])

    # If enemies are still alive, we hold our positions instead.
    if red != 0 and green != 0 and blue != 0:
        output = 0

    return output

def f7(colour, state):
    """
    Prioritise stay on post when enemy is nearby.
    """

    player_pieces = []
    output = 0

    for location in _BORDER_POSTS[colour]:
        if location in state.keys() and state[location] == colour:
            player_pieces.append(location)

    for pq, pr in player_pieces:
        for dq, dr in _ADJACENT_STEPS:
            if (pq + dq, pr + dr) in state and \
            state[(pq + dq, pr + dr)] != colour:
                output += 1

    return output

def hex_distance(location1, location2):
    """
    distance = |q1 - q2| + |r1 - r2 + q1 - q2|
    """
    q1 = location1[0]
    q2 = location2[0]
    r1 = location1[1]
    r2 = location2[1]
    output = abs(q1-q1) + abs(r1-r2+q1-q2)
    return output

def out_of_board(location):
    q = location[0]
    r = location[1]

    return abs(q) > 3 or abs(r) > 3 or abs(q + r) > 3
