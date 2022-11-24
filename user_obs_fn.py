from typing import List, Tuple
from gym.spaces import Space, Box
import numpy as np

from utils import tuple_diff


def observation_space() -> Space:
    return Box(low=0., high=1., shape=(12,), dtype=np.float32)


def get_observation(
        snake: List[Tuple[int]],
        food: Tuple[int],
        prev_snake: List[Tuple[int]],
        prev_food: Tuple[int],
        grid_size: Tuple[int]) -> np.array:
    state = []
    head = snake[-1]
    # Apple is above snake
    # state.append(food[0] < head[0])
    state.append(-1 if food[0] < head[0] else 0 if food[0] == head[0] else 1)# -1 if food is above the head, 1 if right and 0 else
    # Apple is on the left of the snake
    # state.append(food[1] < head[1])
    state.append(-1 if food[1] < head[1] else 0 if food[1] == head[1] else 1)# -1 if food is on the left side of head, 1 if right and 0 else
    # Apple is below the snake
    # state.append(food[0] > head[0])
    state.append(0)
    # Apple is on the right of the snake
    # state.append(food[1] > head[1])
    state.append(0)

    def is_obstacle(pos):
        if pos[0] < 0 or pos[0] >= grid_size[0] or pos[1] < 0 or pos[1] >= grid_size[1] or pos in snake:
            return 1
        return 0
    # obstacle above the snake
    state.append(is_obstacle((head[0] - 1, head[1])))
    # obstacle on the right of the snake
    state.append(is_obstacle((head[0], head[1] + 1)))
    # obstacle below the snake
    state.append(is_obstacle((head[0] + 1, head[1])))
    # obstacle on the left of the snake
    state.append(is_obstacle((head[0], head[1] - 1)))

    snake_dir = tuple_diff(head, snake[-2])

    # direction is up
    # state.append(int(snake_dir == (-1, 0)))
    state.append(-1 if snake_dir == (-1, 0) else 1 if snake_dir == (1, 0) else 0)# -1 if snake is heading up, 1 if down and 0 else
    # state.append(2*head[0]/grid_size[0]-1)

    # direction is right
    # state.append(int(snake_dir == (0, 1)))
    state.append(-1 if snake_dir == (0, -1) else 1 if snake_dir == (0, 1) else 0) # -1 if snake is heading left, 1 if right and 0 else
    # state.append(2*head[1]/grid_size[1]-1)

    # direction is down
    # state.append(int(snake_dir == (1, 0)))
    state.append(0)
    # state.append(2*food[0]/grid_size[0]-1)

    # direction is left
    state.append(0)
    # state.append(2*food[1]/grid_size[1]-1)

    state = np.array(state, dtype=np.float32)

    return state

def wall_proximity(head, grid_size):
    height, width = grid_size
    y, x = head
    y_wall_dist_n, x_wall_dist_n = 4*abs(height/2-y)/height/2, 4*abs(width/2-x)/width/2
    y_n_pow, x_n_pow = np.power(y_wall_dist_n, 4), np.power(x_wall_dist_n, 4)
    return y_n_pow, x_n_pow
