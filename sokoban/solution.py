from sokoban.map import Map


class Solution:
    def __init__(self, steps, solved_map, generated_nodes):
        self.steps = steps
        self.number_of_moves = len(steps)
        self.solved_map = solved_map
        self.generated_nodes = generated_nodes

    def outputActions(self):
        listOfStates = list.copy(self.steps)
        tilesSequence = list(map(lambda x: x[1], listOfStates))

        UP, RIGHT, DOWN, LEFT = 0, 90, 180, 270
        # 2 APPROACHES:
        # 1) Update variable based on how we position robot
        # 2) Always orient robot facing towards UP on board
        orientationCounter = 180

        actions = []
        for tileN in range(1, len(tilesSequence)):
            if tilesSequence[tileN] - tilesSequence[tileN-1] > 1:  # DOWN
                actions.append(DOWN-orientationCounter)
                orientationCounter = DOWN
            elif tilesSequence[tileN] - tilesSequence[tileN-1] == 1:  # RIGHT
                actions.append(RIGHT-orientationCounter)
                orientationCounter = RIGHT
            elif tilesSequence[tileN] - tilesSequence[tileN-1] == -1:  # LEFT
                if orientationCounter == UP:
                    correction = -90
                elif orientationCounter == DOWN:
                    correction = 90
                elif orientationCounter == RIGHT:
                    correction = 180
                else:
                    correction = 0
                actions.append(correction)
                orientationCounter = LEFT
            else:  # UP
                actions.append(90) if orientationCounter == LEFT else actions.append(
                    UP-orientationCounter)
                orientationCounter = UP

            actions.append(
                -1) if listOfStates[tileN][2:] != listOfStates[tileN-1][2:] else None

        # Preprocessing
        i = 0

        while i < len(actions) - 1:
            if actions[i] == -1:
                actions[i+1] = -actions[i+1]
            i += 1

        return actions
