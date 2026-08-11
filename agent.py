import random
from collections import deque


class SimpleReflexAgent:
    """A simple reflex agent that reacts only to the current percept."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here'):
            return 'Up'

        if percept.get('wall_ahead'):
            return 'Left'

        return 'Right'


class ModelBasedAgent:
    """A model-based agent that stores recent state to avoid repeating failures."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
        self._last_percept = None
        self._last_action = None
        self._history = set()
        self._index = 0

    def sense_and_act(self, percept: dict) -> str:
        state_key = (bool(percept.get('wall_ahead')), bool(percept.get('food_here')))

        if state_key in self._history and self._last_action is not None:
            if percept.get('wall_ahead'):
                action = 'Right'
            else:
                action = 'Down'
        else:
            self._history.add(state_key)
            if percept.get('food_here'):
                action = 'Up'
            elif percept.get('wall_ahead'):
                action = 'Left'
            else:
                action = 'Right'

        self._last_percept = percept
        self._last_action = action
        return action


class SearchAgent:
    """Problem-solving agent that uses breadth-first search to plan a path."""

    def __init__(self):
        self.moves = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0),
        }

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        start_x, start_y = start_pos
        goal_x, goal_y = goal_pos
        width, height = grid_size
        walls = set(walls)

        if start_pos == goal_pos:
            return []

        queue = deque([(start_pos, [])])
        visited = {start_pos}

        while queue:
            (x, y), path = queue.popleft()

            for action, (dx, dy) in self.moves.items():
                nx, ny = x + dx, y + dy

                if not (0 <= nx < width and 0 <= ny < height):
                    continue

                next_pos = (nx, ny)
                if next_pos in walls or next_pos in visited:
                    continue

                new_path = path + [action]
                if next_pos == goal_pos:
                    return new_path

                visited.add(next_pos)
                queue.append((next_pos, new_path))

        return None


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
        self._sweep_index = 0

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('smells_food'):
            return 'Up'

        action = self.actions_pool[self._sweep_index]
        self._sweep_index = (self._sweep_index + 1) % len(self.actions_pool)
        return action