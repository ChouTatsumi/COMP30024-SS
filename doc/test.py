board = {(0, 0): 'red', (0, -1): 'red', (-2, 1): 'red', (-1, 0): 'block', (-1, 1): 'block', (1, 1): 'block', (3, -1): 'block'}

pieces = []

child = (2, 3)


items = board.items()
reverse_items = [(v[1], v[0]) for v in items]

print(items)
print(reverse_items)

# for k,v in board.items():
#     if v == 'red':
#         pieces.append(k)

# pieces.pop()

# print(pieces)



# for px, py in pieces:
#     print("({}, {})".format(px, py))
#     print(type(px))
#     print(px)

# for kx, ky, v in board.items():
#     print("({}, {}): {}".format(kx, ky, v))
