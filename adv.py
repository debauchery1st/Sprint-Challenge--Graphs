from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def make_keys():
    e = player.current_room.get_exits()
    return dict(zip(e, ['?'] * len(e)))


tgraph = {}

# Start by writing an algorithm that
# picks a random unexplored direction from the player's current room,


def pick_room():
    available = tgraph.get(player.current_room.id, make_keys())
    tgraph[player.current_room.id] = available
    unexplored = [k for k, v in available.items() if v == '?']
    if len(unexplored) > 0:
        return unexplored.pop()
    return None


def check_keys(limit=None):
    if limit == None:
        return "requires integer limit"
    if len(tgraph) == limit:
        for _, keys in tgraph.items():
            for _, v in keys.items():
                if v == "?":
                    return False
        return True
    return False

# travels and logs that direction, then loops.


def travel_log():
    re = [None]  # keep track of the way back
    b = True
    # count = 0
    while b is not None:
        b = pick_room()
        if b is not None:
            a = int(player.current_room.id)
            player.travel(b)
            traversal_path.append(b)  # log
            wb = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}[b]
            re.append(wb)  # the way back
            tgraph[a][b] = int(player.current_room.id)
        else:
            b = re.pop()
            # count += 1
            if check_keys(500):
                # check to see if we have explored 500 rooms,
                print("STOPPED AT ROOM ", player.current_room.id)
                return
            if b is not None:
                traversal_path.append(b)
                player.travel(b)
    print("STOPPED AT ROOM ", player.current_room.id)


travel_log()
#
# This should cause your player to walk a depth-first traversal.
#
# When you reach a dead-end (i.e. a room with no unexplored paths),
# walk back to the nearest room that does contain an unexplored path.


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
