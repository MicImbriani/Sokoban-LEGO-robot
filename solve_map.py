from sokoban.map_parser import MapParser
from sokoban.solver import Solver
from sokoban.solution_plotter import print_solution
import os
import pickle


def save_solution_to_file(filename, solution):
    with open(filename + ".pickle", "wb") as outfile:
        # "wb" argument opens the file in binary mode
        pickle.dump(solution, outfile)


if __name__ == "__main__":
    parser = MapParser()
    # map_file_path = "./maps/map_01_one_can.txt"
    # map_file_path = "./maps/map_02_two_cans.txt"
    # map_file_path = "./maps/map_03_robot_on_goal.txt"
    # map_file_path = "./maps/map_04_push_through_test.txt"
    # map_file_path = "./maps/map_05_from_pdf.txt"
    # map_file_path = "./maps/map_08_real.txt"
    map_file_path = "./maps/MAP_COMPETITION.txt"
    parsed_map = parser.parse(map_file_path)

    solver = Solver(parsed_map)
    solution = solver.solve(visually=False, show_visited_count=True)
    save_solution_to_file("maps/solutions/" +
                          os.path.basename(map_file_path), solution)
    print_solution(solution, animate=True)

    actions = solution.outputActions()
    print(actions)
