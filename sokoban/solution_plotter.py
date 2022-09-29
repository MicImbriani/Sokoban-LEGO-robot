from sokoban.solution import Solution
from sokoban.map import Map
import os
import time


def print_map_from_char_list(chars, map_size):
    for i in range(1, len(chars)):
        print(chars[i], end="")

        if i % map_size == 0:
            print("\n", end="")


def print_step(parsed_map: Map, step, animate=False):
    map_chars = list.copy(parsed_map.static_chars)
    robot_tile_id = step[1]
    map_chars[robot_tile_id] = '@'
    can_tile_ids = step[2:]
    goal_tile_ids = parsed_map.goals

    for goal_tile_id in goal_tile_ids:
        map_chars[goal_tile_id] = '.'

    for can_tile_id in can_tile_ids:
        if map_chars[can_tile_id] == '.':
            map_chars[can_tile_id] = '*'
        else:
            map_chars[can_tile_id] = '$'

    if animate:
        os.system('cls||clear')

    print_map_from_char_list(map_chars, parsed_map.size)
    print("\n")


def print_solution(solution: Solution, animate=False):
    for step in solution.steps:
        print_step(solution.solved_map, step, animate)

        if animate:
            time.sleep(0.250)

    print("Total generated nodes: " + str(solution.generated_nodes))
    print("Solution's number of moves: " + str(solution.number_of_moves))
