from sokoban.solution_plotter import print_solution
import sys
import pickle


if __name__ == "__main__":
    file_name = "maps/solutions/map_01_one_can.txt"

    with open(file_name + ".pickle", "rb") as infile:
        solution = pickle.load(infile)

    print_solution(solution)