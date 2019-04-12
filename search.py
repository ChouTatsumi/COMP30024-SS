"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
Group Sandscuplture
Liu Xiaohan, xiaohanl4, 908471
Zhang Xun, xunz4, 854776
"""

import sys
import json

direction_list = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, index, movement, parent = None):
        self.index = index
        self.movement = movement
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.index == other.index

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: Search for and output winning sequence of moves
    # ...

    # convert data to state
    init_state = {}

    for qr in data['blocks']:
        init_state[(qr[0], qr[1])] = 'block'
    for qr in data['pieces']:
        init_state[(qr[0], qr[1])] = data['colour']

    # search for path
    for qr in data['pieces']:
        index = (qr[0], qr[1])
        path = astar(index, data['colour'], init_state)
        print_path(path)

    # test for data input
    # print(data['pieces'])
    # print(exitable('red', [3, -3]))
    # print(exitable(data['colour'], data['pieces'][0]))

    # board = {(0, 0) : 'red', (0, -1) : 'red', (-2, 1) : 'red', (-1, 0) : 'block', (-1, 1) : 'block', (1, 1) : 'block', (3, -1) : 'block'}
    # print_board(board)

def astar(index, colour, state):
    # Initialize both open and closed list
    open_list = []
    close_list = []

    #Add the start node
    start_node = Node(index, 'START', None)
    start_node.state = state
    start_node.g = 0
    start_node.h = heuristic(index, colour, state)
    start_node.f = start_node.g + start_node.h

    open_list.append(start_node)

    while len(open_list) > 0:

        # Get the current node
        curr_node = open_list[0]
        curr_i = 0
        for i, item in enumerate(open_list):
            if item.f < curr_node.f:
                curr_node = item
                curr_i = i

        # Add current node to close list from open list
        open_list.pop(curr_i)
        close_list.append(curr_node)
        
        # Find the goal
        if exitable(colour, curr_node.index):
            path = []
            current = curr_node
            while current is not None:
                path.append(current)
                current = current.parent
            return path[::-1]

        # Generate children
        children = []
        children_dic = possible_dest(state, curr_node.index)
        for (key, value) in children_dic.items():
            new_node = Node(key, value, curr_node)
            children.append(new_node)

        # evaluate the cost of each child
        for child in children:

            for node in close_list:
                if child == node:
                    continue

            child.g = curr_node.g + 1
            child.h = heuristic(child.index, colour, state)
            child.f = child.g + child.h

            for node in open_list:
                if child == node and child.g > node.g:
                    continue

            open_list.append(child)


def heuristic(index, colour, state):
    """
    This is a function to calculate the true distance from index to any
    terminal
    """
    output = 0

    A_list = []
    B_list = []

    q = index[0]
    r = index[1]

    if colour == 'red':
        output = 3 - q

        while(q < 3 and q + r < 3):
            q += 1
            A_list.append((q, r))
        while(q < 3):
            q += 1
            r -= 1
            A_list.append((q, r))
        
        q = index[0]
        r = index[1]
        while(q < 3 and r > -3):
            q += 1
            r -= 1
            B_list.append((q, r))
        while(q < 3):
            q += 1
            B_list.append((q, r))

        A_offset = offset(A_list, state)
        B_offset = offset(B_list, state)

        output += min(A_offset, B_offset)

    elif colour == 'green':
        output = 3 - r

        while(r < 3 and q + r < 3):
            r += 1
            A_list.append((q, r))
        while(r < 3):
            q -= 1
            r += 1
            A_list.append((q, r))

        q = index[0]
        r = index[1]
        while(r < 3 and q > -3):
            q -= 1
            r += 1
            B_list.append((q, r))
        while(r < 3):
            r += 1
            B_list.append((q, r))

        A_offset = offset(A_list, state)
        B_offset = offset(B_list, state)

        output += min(A_offset, B_offset)

    elif colour == 'blue':
        output = q + r + 3

        while(q + r > -3 and q > -3):
            q -= 1
            A_list.append((q, r))
        while(q + r > -3):
            r -= 1
            A_list.append((q, r))

        q = index[0]
        r = index[1]
        while(q + r > -3 and r > -3):
            r -= 1
            B_list.append((q, r))
        while(q + r > -3):
            q -= 1
            B_list.append((q, r))

        A_offset = offset(A_list, state)
        B_offset = offset(B_list, state)

        output += min(A_offset, B_offset)

    return output

def offset(lst, state):
    output = 0
    flag = False

    for i in range(0, len(lst) - 1):
        if lst[i] in state.keys():
            if not flag:
                flag = True
                output -= 1
            else:
                output += 2
        else:
            if flag:
                flag = False

    return output

def print_path(path):
    start_node = path[0]

    if start_node.movement != 'START':
        print("ERROR: path list didn't start at start node.")

    last_index = start_node.index

    for i in range(1, len(path)):
        node = path[i]
        print('{} from {} to {}.'.format(node.movement, last_index, node.index))
        last_index = node.index

    print('EXIT from {}.'.format(last_index))
    return path

def exitable(colour, index):
    if colour == 'red' and index[0] == 3 or \
        colour == 'green' and index[1] == 3 or \
            colour == 'blue' and index[0] + index[1] == -3:
        return True
    return False

def moveable(state, index_curr, index_dest):
    #see if destination is occupied
    if index_dest in state.keys():
        return False
    #see if destination is in move range
    for index in direction_list:
        if index_dest[0] == (index_curr[0] + index[0]) and \
            index_dest[1] == (index_curr[1] + index[1]):
            return True
    #return False by default
    return False

def jumpable(state, index_curr, index_dest):
    #see if destination is occupied
    if index_dest in state.keys():
        return False
    #see if destination is in jump range
    if ((index_dest[0] - index_curr[0]) % 2) == 0 and \
        ((index_dest[1] - index_curr[1]) % 2) == 0 and \
        (index_dest[0] - index_curr[0]) < 3 and \
            (index_dest[1] - index_curr[1]) < 3:
        return True
    #return False by default
    return False

def possible_dest(state, index_curr):
    dest_dic = {}
    # index_dest = ()
    #see what's in move range
    for index in direction_list:
        #let dest be one of six locations in move range
        index_dest = (index_curr[0] + index[0], index_curr[1] + index[1])
        #see if dest is occupied with an obstacle
        if moveable(state, index_curr, index_dest):
            dest_dic[index_dest] = "MOVE"
        else:
            #let dest be the location behind that obstacle
            index_dest = (index_curr[0] + index[0], index_curr[1] + index[1])
            #see if dest is occupied with an obstacle
            if jumpable(state, index_curr, index_dest):
                dest_dic[index_dest] = "JUMP"
    
    return dest_dic

def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}|
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}|
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} |
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
