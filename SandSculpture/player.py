from SandSculpture import eval

_FINISHING_HEXES = {
    'red': [(3, -3), (3, -2), (3, -1), (3, 0)],
    'green': [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
    'blue': [(-3, 0), (-2, -1), (-1, -2), (0, -3)]
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

        for k, v in self.state:
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
            for dq, dr in eval._ADJACENT_STEPS:
                child = (q + dq, r + dr)
                if not (child in self.state or eval.out_of_board(child)):
                    action = ("MOVE", ((q, r), child))
                    new_state = self.state.copy()
                    new_state[child] = self.colour
                    new_state.pop((q, r))
                    actions[action] = eval.eval(self.colour, new_state)
                elif child in self.state:
                    child = (child[0] + dq, child[1] + dr)
                    if not (child in self.state or eval.out_of_board(child)):
                        action = ("JUMP", ((q, r), child))
                        new_state = self.state.copy()
                        new_state[child] = self.colour
                        new_state[((child[0] + q) / 2,
                                   (child[1] + r) / 2)] = self.colour
                        new_state.pop((q, r))
                        actions[action] = eval.eval(self.colour, new_state)

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
