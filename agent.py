import torch
import random
import numpy as np
from collections import deque
from AI import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

# Hyperparameters
MEMORY_CAPACITY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class SnakeAgent:
    def __init__(self):
        self.games_played = 0
        self.exploration_rate = 0  # Initial epsilon
        self.discount_factor = 0.9  # Gamma for future rewards
        self.replay_memory = deque(maxlen=MEMORY_CAPACITY)
        self.neural_model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.neural_model, lr=LEARNING_RATE, gamma=self.discount_factor)

    def extract_state(self, game_instance):
        snake_head = game_instance.snake[0]
        adjacent_left = Point(snake_head.x - 20, snake_head.y)
        adjacent_right = Point(snake_head.x + 20, snake_head.y)
        adjacent_up = Point(snake_head.x, snake_head.y - 20)
        adjacent_down = Point(snake_head.x, snake_head.y + 20)

        is_moving_left = game_instance.direction == Direction.left
        is_moving_right = game_instance.direction == Direction.right
        is_moving_up = game_instance.direction == Direction.up
        is_moving_down = game_instance.direction == Direction.down

        state_representation = [
            (is_moving_right and game_instance.detect_collision(adjacent_right)) or 
            (is_moving_left and game_instance.detect_collision(adjacent_left)) or 
            (is_moving_up and game_instance.detect_collision(adjacent_up)) or 
            (is_moving_down and game_instance.detect_collision(adjacent_down)),

            (is_moving_up and game_instance.detect_collision(adjacent_right)) or 
            (is_moving_down and game_instance.detect_collision(adjacent_left)) or 
            (is_moving_left and game_instance.detect_collision(adjacent_up)) or 
            (is_moving_right and game_instance.detect_collision(adjacent_down)),

            (is_moving_down and game_instance.detect_collision(adjacent_right)) or 
            (is_moving_up and game_instance.detect_collision(adjacent_left)) or 
            (is_moving_right and game_instance.detect_collision(adjacent_up)) or 
            (is_moving_left and game_instance.detect_collision(adjacent_down)),

            is_moving_left,
            is_moving_right,
            is_moving_up,
            is_moving_down,
            
            game_instance.food.x < snake_head.x,
            game_instance.food.x > snake_head.x,
            game_instance.food.y < snake_head.y,
            game_instance.food.y > snake_head.y
        ]

        return np.array(state_representation, dtype=int)

    def store_experience(self, state, action, reward, next_state, terminal):
        self.replay_memory.append((state, action, reward, next_state, terminal))

    def replay_experience(self):
        sample_batch = random.sample(self.replay_memory, BATCH_SIZE) if len(self.replay_memory) > BATCH_SIZE else self.replay_memory
        batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones = zip(*sample_batch)
        self.trainer.train_step(batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones)

    def immediate_experience(self, state, action, reward, next_state, terminal):
        self.trainer.train_step(state, action, reward, next_state, terminal)

    def choose_action(self, current_state):
        self.exploration_rate = max(0, 80 - self.games_played)
        decision_vector = [0, 0, 0]
        if random.randint(0, 200) < self.exploration_rate:
            chosen_action = random.randint(0, 2)
            decision_vector[chosen_action] = 1
        else:
            state_tensor = torch.tensor(current_state, dtype=torch.float)
            prediction = self.neural_model(state_tensor)
            chosen_action = torch.argmax(prediction).item()
            decision_vector[chosen_action] = 1

        return decision_vector


def train_agent():
    score_history = []
    avg_score_history = []
    cumulative_score = 0
    highest_score = 0
    agent = SnakeAgent()
    game_instance = SnakeGameAI()
    
    while True:
        prev_state = agent.extract_state(game_instance)
        move = agent.choose_action(prev_state)
        reward, game_over, current_score = game_instance.step(move)
        next_state = agent.extract_state(game_instance)
        
        agent.immediate_experience(prev_state, move, reward, next_state, game_over)
        agent.store_experience(prev_state, move, reward, next_state, game_over)

        if game_over:
            game_instance.initialize_game()
            agent.games_played += 1
            agent.replay_experience()

            if current_score > highest_score:
                highest_score = current_score
                agent.neural_model.save()

            print(f'Game {agent.games_played}, Score: {current_score}, Record: {highest_score}')
            
            score_history.append(current_score)
            cumulative_score += current_score
            mean_score = cumulative_score / agent.games_played
            avg_score_history.append(mean_score)
            plot(score_history, avg_score_history)


if __name__ == '__main__':
    train_agent()
