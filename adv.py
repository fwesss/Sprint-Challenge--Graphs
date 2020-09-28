import random
import sys
import time
from ast import literal_eval

from player import Player
from world import World


def traverse(iterations=1) -> None:
    start_time = time.time()
    possible_paths = []

    for _ in range(iterations):
        player = Player(world.starting_room)

        traversal_path = []

        inverse = {"n": "s", "e": "w", "s": "n", "w": "e"}
        visited = {
            player.current_room.id: {
                "visits": 1,
                "directions": {
                    direction: 4 for direction in player.current_room.get_exits()
                },
            }
        }

        while len(visited) < len(room_graph):
            max_visits = max(
                visited[player.current_room.id]["directions"].items(),
                key=lambda x: x[1],
            )

            list_of_keys = []
            for key, value in visited[player.current_room.id]["directions"].items():
                if value == max_visits[1]:
                    list_of_keys.append(key)

            direction = random.choice(list_of_keys)

            previous_room = player.current_room
            player.travel(direction)
            traversal_path.append(direction)

            if player.current_room.id not in visited:
                visited[player.current_room.id] = {
                    "visits": 1,
                    "directions": {
                        direction: 4 for direction in player.current_room.get_exits()
                    },
                }
            else:
                visited[player.current_room.id]["visits"] += 1

            visited[player.current_room.id]["directions"][inverse[direction]] -= 1
            visited[previous_room.id]["directions"][direction] -= 1

        # TRAVERSAL TEST - DO NOT MODIFY
        visited_rooms = set()
        player.current_room = world.starting_room
        visited_rooms.add(player.current_room)

        for move in traversal_path:
            player.travel(move)
            visited_rooms.add(player.current_room)

        if len(visited_rooms) == len(room_graph):
            print(
                f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
            )
        else:
            print("TESTS FAILED: INCOMPLETE TRAVERSAL")
            print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

        possible_paths.append(traversal_path)

    path_file = open("best-path.txt", "r")
    first, *middle, last = path_file.read().split()

    if len(min(possible_paths, key=len)) < int(last):
        print(min(possible_paths, key=len), file=open("best-path.txt", "w"))
        print(len(min(possible_paths, key=len)), file=open("best-path.txt", "a"))
        print(
            f"\nShortest path found was {len(min(possible_paths, key=len))} moves long.\nThis is shortest path found yet so it was written to 'best-path.txt'\n"
        )
    else:
        print(
            f"\nShortest path found was {len(min(possible_paths, key=len))} moves long.\nThis is longer than the previous shortest path of {last}.\n"
        )

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
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

    world.print_rooms()

    traverse(int(sys.argv[1]))

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
