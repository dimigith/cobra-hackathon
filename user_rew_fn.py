from typing import List, Tuple

MAX_STEPS_EXCEEDED_REW = -1
MAX_REPEAT_MOVE_EXCEEDED_REW = -1

from user_obs_fn import get_observation


def get_reward(
        snake: List[Tuple[int]],
        food: Tuple[int],
        prev_snake: List[Tuple[int]],
        prev_food: Tuple[int],
        grid_size: Tuple[int],
        is_done: bool) -> float:

    # If game over, give negative reward
    if is_done:
        return -1

    prev_head = prev_snake[-1]
    new_head = snake[-1]

    # The snake has eaten an apple if it's new head position is the
    # same as the previous food position
    has_eaten = prev_food == new_head

    if has_eaten:
        return 1

    # To make the reward less sparse, give the agent positive reward
    # if it got closer to the food, negative if it got further away
    prev_dist = abs(food[0] - prev_head[0]) + abs(food[1] - prev_head[1])
    new_dist = abs(food[0] - new_head[0]) + abs(food[1] - new_head[1])

    # closeness_reward = 1-len(snake)/(grid_size[0]*grid_size[1]) # 0.1
    # distance_from_food = (48-(abs(food[0] - new_head[0]) + abs(food[1] - new_head[1])))/48

    # rew = 0.1 if new_dist < prev_dist else -0.3
    # rew = 0.4*distance_from_food

    obs = get_observation(snake, food, prev_snake, prev_food, grid_size)

    heading_towards_food_reward_y = 1 if obs[0]*obs[8] > 0 else 0 if obs[0]*obs[8]==0 else -3
    heading_towards_food_reward_x = 1 if obs[1]*obs[9] > 0 else 0 if obs[1]*obs[9]==0 else -3
    heading_towards_food_reward = heading_towards_food_reward_y + 1.1*heading_towards_food_reward_x

    getting_closer_reward = 1 if new_dist < prev_dist else -3

    hugging_obstacles_reward = 1 if obs[5] or obs[7] else 0

    # facing_an_obstacle_reward = -obs[2]#is_facing_an_obstacle(obs[8:10], obs[4:8])
    # if facing_an_obstacle_reward<0:
    #     print('asdd')

    rew = 0.05*getting_closer_reward+0.05*heading_towards_food_reward#+0.3*facing_an_obstacle_reward

    return rew


def is_facing_an_obstacle(yx_dir, urdl_obstacle_flag):
    y_dir, x_dir = yx_dir
    up_flag, right_flag, down_flag, left_flag = urdl_obstacle_flag

    if y_dir == -1 and up_flag:
        return 1

    if y_dir == 1 and down_flag:
        return 1

    if x_dir == -1 and left_flag:
        return 1

    if x_dir == 1 and right_flag:
        return 1

    return 0


