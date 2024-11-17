# Snake AI Game

This repository contains an AI-powered Snake game built using Python, PyGame, and PyTorch. The AI agent is trained using a reinforcement learning algorithm to learn and play the classic Snake game autonomously.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)
- [Conclusion](#conclusion)

## Introduction
The Snake AI game leverages reinforcement learning techniques to train an agent that can play the game with minimal human intervention. The AI agent makes decisions based on its current state to maximize its score while avoiding collisions.

## Features
- **Reinforcement Learning Agent**: Trained using a custom neural network.
- **PyGame Interface**: Interactive gameplay visualization.
- **Performance Tracking**: Displays scores and tracks high scores during training.
- **Modular Codebase**: Easy to modify and extend for further experimentation.

## Requirements
Ensure that you have Python 3.8 or higher installed. The following Python libraries are needed:

- `pygame`
- `torch`
- `numpy`
- `matplotlib`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/snake-ai-game.git
   cd snake-ai-game
   ```
2. Install the required Python packages individually:
   ```bash
   pip install pygame torch numpy matplotlib
   ```

## How to Run
1. To train the AI agent, run:
   ```bash
   python agent.py
   ```
2. The game window will open, and you can observe the AI playing and learning.

## Project Structure
```
|-- snake-ai-game
    |-- agent.py        # Main script for training the AI
    |-- model.py        # Defines the neural network architecture
    |-- AI.py           # Contains the logic for AI decision-making
    |-- game.py         # Core game mechanics using PyGame
    |-- README.md       # Project documentation
```

## Technical Details
- **Neural Network**: Implemented using PyTorch, consisting of fully connected layers to process game state inputs and output action probabilities.
- **State Representation**: The game state includes the current direction, position of the snake, and location of food.
- **Training Algorithm**: Utilizes Q-learning for training the AI agent, updating weights based on the reward obtained at each step.

### Example Code Snippet
```python
state = get_game_state()
action = agent.select_action(state)
reward, done = game.step(action)
agent.train_step(state, action, reward, next_state, done)
```

## Conclusion
This project demonstrates the potential of reinforcement learning in creating intelligent agents capable of playing games autonomously. By integrating PyTorch and PyGame, the Snake AI Game provides a hands-on example of how machine learning concepts can be applied to game development. Whether you're looking to learn more about reinforcement learning or enhance the AI further, this project offers a strong foundation for experimentation and learning.

---
Thank you for checking out the Snake AI Game!
