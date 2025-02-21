# backend/rl_progress.py
import numpy as np
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['learning_path']



class QLearning:
    def __init__(self):
        self.states = [1, 2, 3]  # Difficulty levels
        self.actions = ['stay', 'increase', 'decrease']
        self.Q = np.zeros((len(self.states), len(self.actions)))
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor

    def get_action(self, state):
        if state < 0 or state >= len(self.states):
            state = 1  # Default to middle state if invalid
        action_idx = np.argmax(self.Q[state])
        return min(max(action_idx, 0), len(self.actions) - 1)  # Ensure valid action index



    def update(self, state, action, reward, next_state):
        if state < 0 or state >= len(self.states) or next_state < 0 or next_state >= len(self.states):
            return  # Skip update for invalid states
        action_idx = self.actions.index(action)
        self.Q[state, action_idx] += self.alpha * (reward + self.gamma * np.max(self.Q[next_state]) - self.Q[state, action_idx])


# Global instance
q_learner = QLearning()

def update_progress(student_id, lesson_id, score):
    # Get current difficulty and validate
    lesson = db.lessons.find_one({'id': lesson_id}, {'difficulty': 1})
    if lesson is None:
        print("No lesson available with ID:", lesson_id)
        return {'error': 'No lesson available'}, 404
    difficulty = lesson['difficulty']


    current_difficulty = max(0, min(difficulty - 1, len(q_learner.states) - 1))  # Ensure valid state


    
    # Insert progress with validation
    try:
        db.progress.insert_one({
            'student_id': student_id,
            'lesson_id': lesson_id,
            'score': score,
            'completed': True
        })
    except PyMongoError as e:
        print(f"Error inserting progress: {e}")
        return


    
    # Determine reward and next action
    reward = score - 50  # Positive reward if score > 50
    action_idx = q_learner.get_action(current_difficulty)
    action = q_learner.actions[action_idx]  # Get action name from index
    next_difficulty = max(0, min(current_difficulty + (1 if action == 'increase' else -1 if action == 'decrease' else 0), len(q_learner.states) - 1))


    
    # Update Q-table
    try:
        q_learner.update(current_difficulty, action, reward, next_difficulty)
    except Exception as e:
        print(f"Error updating Q-table: {e}")
