from sokoban.solution import Solution
from sokoban.solution_plotter import print_step


class Solver:
    nodes_visited: int = 0
    queue_to_expand = []
    list_of_expanded = []

    def __init__(self, map_to_solve):
        self.map_to_solve = map_to_solve
        self.goals = map_to_solve.goals
        self.walls = map_to_solve.walls
        self.cans = map_to_solve.cans
        self.robot = map_to_solve.robot[0]
        self.chars = map_to_solve.chars
        self.static_chars = map_to_solve.static_chars
        self.map_size = map_to_solve.size
        self.map_file_path = map_to_solve.map_file_path
        self.last_tile_id = self.map_size * self.map_size

    @staticmethod
    def is_goal_state(cans, goals):
        goals_set = set(goals)
        cans_set = set(cans)

        all_goals_have_cans = len(goals_set.difference(cans_set)) == 0
        all_cans_on_goals = len(cans_set.difference(goals_set)) == 0

        return all_goals_have_cans or all_cans_on_goals

    def is_wall(self, tile_id: int) -> bool:
        return self.chars[tile_id] == "X" or self.chars[tile_id] == "#"

    def is_can(self, tile_id: int, cans) -> bool:
        return tile_id in cans

    def is_out_of_bounds(self, tile_id: int) -> bool:
        return (tile_id < 1) or (tile_id > self.last_tile_id)

    def is_occupied(self, tile_id: int):
        return not (self.chars[tile_id] == ' ' or self.chars[tile_id] == '.')

    def get_actions(self, tile_id: int, cans):
        """
        :param tile_id: The tile to check actions for
        :param cans: list of the current can positions
        :return: A list of IDs of destination tiles (negative ID ==> not a valid action)
        """
        # neighbors = [UP, DOWN, LEFT, RIGHT]
        neighbors = [tile_id - self.map_size, tile_id + self.map_size, tile_id - 1, tile_id + 1]
        second_neighbors = [tile_id - self.map_size * 2, tile_id + self.map_size * 2, tile_id - 2, tile_id + 2]
        action_validity = neighbors.copy()

        for index, tile in enumerate(neighbors):
            if self.is_out_of_bounds(tile) or self.is_wall(tile):
                action_validity[index] = -1
            if self.is_can(tile, cans) and self.is_occupied(second_neighbors[index]):
                action_validity[index] = -1

        return action_validity

    @staticmethod
    def update_can_tile_ids(selected_node, action):
        """
        Given a state and an action, returns an updated list of can positions.

        :param selected_node: Current state
        :param action: Tile ID of the robots next position
        :return: Updated list of can positions (tile IDs)
        """
        cans = list.copy(selected_node[2:])

        for index, can_tile_id in enumerate(cans):
            if can_tile_id == action:
                cans[index] += action - selected_node[1]
        return cans

    def is_node_in_list(self, searched_node, list):
        for node in list:
            if searched_node[1:] == node[1:]:
                return True

        return False

    # Checks if the given state exists.
    def does_state_exist(self, selected_node):
        in_queue = self.is_node_in_list(selected_node, self.queue_to_expand)
        in_list = self.is_node_in_list(selected_node, self.list_of_expanded)

        if in_queue or in_list:
            return True
        return False

    def get_path(self, last_node, path=[]):
        if last_node is None:
            return path
        else:
            return self.get_path(last_node[0], path + [last_node])

    # BFS pseudo-code:
    # ===========================================
    # 1. Put the first node into the queue
    # 2. If "queue_to_expand" is empty then there is no solution
    # 3. Select the first node in the "queue_to_expand"
    # 4. If the selected node is the goal state then finish and return the path to the root in reverse order
    # 5. Expand the selected node and place the descendants into "queue_to_expand"
    #    if they are not already in the "queue_to_expand" or the "list_of_expanded".
    #    Place the expanded node into the "list_of_expanded" and jump to step 2.

    # Returns a list of nodes from goal to start or empty list if no solution found
    def bfs(self, visually: bool, show_visited_count: bool):
        """
        # State is a list where:
        # - index 0 = reference to the parent node
        # - index 1 = tileID of the robot position
        # - index 2... = cans
        # e.g. [parent_node, robot, can_1, can_2, can_3, ...]
        :return: A list of nodes from start to finish.
        """

        # 1.
        self.queue_to_expand.insert(0, [None, self.robot] + self.cans)

        while True:
            # 2.
            if len(self.queue_to_expand) == 0:
                print("All nodes explored and no solution found.")
                return []

            # 3.
            # The oldest element is on the last index
            selected_node = self.queue_to_expand.pop()

            self.nodes_visited += 1
            if self.nodes_visited % 500 == 0:
                print("Nodes visited: " + str(self.nodes_visited))
                print("Total node count: " + str(len(self.queue_to_expand) + len(self.list_of_expanded)), end="\n\n")

            if visually:
                print_step(self.map_to_solve, selected_node)

            # 4.
            if self.is_goal_state(selected_node[2:], self.goals):
                return list(reversed(self.get_path(selected_node)))

            # 5.
            actions = self.get_actions(selected_node[1], selected_node[2:])

            for action in actions:
                # If it is a valid action...
                if action > 0:
                    child_node = [selected_node, action] + self.update_can_tile_ids(selected_node, action)

                    if not self.does_state_exist(child_node):
                        self.queue_to_expand.insert(0, child_node)  # Child into queue

            self.list_of_expanded.append(selected_node)  # Parent into expanded list

    def solve(self, visually: bool, show_visited_count: bool):
        solution_steps = self.bfs(visually, show_visited_count)
        generated_nodes = len(self.queue_to_expand) + len(self.list_of_expanded)
        return Solution(solution_steps, self.map_to_solve, generated_nodes)
