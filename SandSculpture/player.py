# Game-algorithm-specific constants:
_ADJACENT_STEPS = [(-1, +0), (+0, -1), (+1, -1), (+1, +0), (+0, +1), (-1, +1)]

_FINISHING_HEXES = {
    'red': [(3, -3), (3, -2), (3, -1), (3, 0)],
    'green': [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
    'blue': [(-3, 0), (-2, -1), (-1, -2), (0, -3)]
}

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


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.state = {(-3, 3): 'red', (-3, 2): 'red', (-3, 1): 'red', (-3, 0): 'red',
                      (0, -3): 'green', (1, -3): 'green', (2, -3): 'green', (3, -3): 'green',
                      (3, 0): 'blue', (2, 1): 'blue', (1, 2): 'blue', (0, 3): 'blue'}
        self.ready_to_exit = 0

    def action(self):
        # TODO: Decide what action to take.

        # dictionaries store actions and its evaluation value
        actions = {}

        # generate action nodes (children)
        pieces = []

        for k, v in self.state.items():
            if v == self.colour:
                pieces.append(k)

        # Prioritise EXIT when we are the only surviver
        if self.ready_to_exit < 4:
            count = 0
            for post in _FINISHING_HEXES[self.colour]:
                if post in self.state.keys() and self.state[post] == self.colour:
                    count += 1
            self.ready_to_exit = count
        elif self.ready_to_exit > 4:
            print("Player arguments error")
            exit(-1)

        if self.ready_to_exit == 4:
            for post in _FINISHING_HEXES[self.colour]:
                if post in self.state.keys() and self.state[post] == self.colour:
                    return ("EXIT", post)

        # Normal situation
        for q, r in pieces:
            for dq, dr in _ADJACENT_STEPS:
                child = (q + dq, r + dr)
                if not (child in self.state or self.out_of_board(child)):
                    action = ("MOVE", ((q, r), child))
                    new_state = self.state.copy()
                    new_state[child] = self.colour
                    new_state.pop((q, r))
                    actions[action] = self.evaluate(self.colour, new_state)
                    print(actions)
                elif child in self.state:
                    child = (child[0] + dq, child[1] + dr)
                    if not (child in self.state or self.out_of_board(child)):
                        action = ("JUMP", ((q, r), child))
                        new_state = self.state.copy()
                        new_state[child] = self.colour
                        new_state[((child[0] + q) / 2,
                                   (child[1] + r) / 2)] = self.colour
                        new_state.pop((q, r))
                        actions[action] = self.evaluate(self.colour, new_state)

        # Have to EXIT
        if len(actions) == 0:
            for post in _FINISHING_HEXES[self.colour]:
                if post in pieces:
                    return ("EXIT", post)
            # Have to PASS
            return ("PASS", None)

        # return the action with max evaluation value
        # sort actions dictionary by value
        items = actions.items()
        # gernerate a list in form of [(value, action)]
        reverse_items = [(v[1], v[0]) for v in items]
        reverse_items.sort(reverse = True)

        return reverse_items[0][1]

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        You may assume that action will always correspond to an allowed action
        (or pass) for the player colour (your method does not need to validate
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.
        if action[0] == "MOVE":
            self.state[action[1][1]] = colour
            self.state.pop(action[1][0])
        elif action[0] == "JUMP":
            self.state[action[1][1]] = colour
            self.state.pop(action[1][0])
            q = (action[1][1][0] + action[1][0][0])/2
            r = (action[1][1][1] + action[1][0][1])/2
            self.state[(q,r)] = colour
        elif action[0] == "EXIT":
            self.state.pop(action[1])

    def evaluate(self, colour, state):
        w1 = 10
        w2 = 3
        w3 = -1
        w4 = -100
        w5 = 20
        w6 = 5
        w7 = 300

        return w1 * self.f1(colour, state) + w2 * self.f2(colour, state) + \
            w3 * self.f3(colour, state) + w4 * self.f4(colour, state) + \
            w5 * self.f5(colour, state) + w6 * self.f6(colour, state) + \
            w7 * self.f7(colour, state)

    def f1(self, colour, state):
        """
        How many pieces of ours are at border posts.
        """
        output = 0

        for location in _BORDER_POSTS[colour]:
            if location in state.keys() and state[location] == colour:
                output += 1

        return output

    def f2(self, colour, state):
        """
        How many pieces of ours are at edges.
        """
        output = 0

        for (q, r), v in state.items():
            if v == colour:
                if abs(q) == 3 or abs(r) == 3 or abs(q + r) == 3:
                    output += 1

        return output

    def f3(self, colour, state):
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
                d = self.hex_distance(post, player_pieces[i])
                if d < min_distance:
                    min_distance = d
                    min_idx = i

            if len(player_pieces) > 0:
                output += min_distance
                player_pieces.pop(min_idx)

        return output

    def f4(self, colour, state):
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
                    if not (opposite in state or self.out_of_board(opposite)):
                        output += 1

        return output

    def f5(self, colour, state):
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

    def f6(self, colour, state):
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

    def f7(self, colour, state):
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

    def hex_distance(self, location1, location2):
        """
        distance = |q1 - q2| + |r1 - r2 + q1 - q2|
        """
        q1 = location1[0]
        q2 = location2[0]
        r1 = location1[1]
        r2 = location2[1]
        output = abs(q1-q1) + abs(r1-r2+q1-q2)
        return output

    def out_of_board(self, location):
        q = location[0]
        r = location[1]

        return abs(q) > 3 or abs(r) > 3 or abs(q + r) > 3