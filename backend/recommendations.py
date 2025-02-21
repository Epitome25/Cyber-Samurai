import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

def vectorize(interests):
    # Simple vectorization: 1 if skill/interest present, 0 otherwise
    skills_list = ['math', 'science', 'art', 'creativity']
    return [1 if skill in interests else 0 for skill in skills_list]

def recommend_career(interests):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['learning_path']
    
    # Get all careers
    careers = list(db.careers.find({}, {'name': 1, 'required_skills': 1}))
    
    student_vector = np.array([vectorize(interests)])
    career_vectors = np.array([vectorize(career['required_skills']) for career in careers])
    
    similarities = cosine_similarity(student_vector, career_vectors)
    recommended_index = np.argmax(similarities)
    
    return careers[recommended_index]['name']

def recommend_next_lesson(student_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['learning_path']
    
    # Get student progress
    progress = list(db.progress.find({'student_id': student_id}, {'lesson_id': 1, 'score': 1}))
    
    if not progress:
        # Start with easiest lesson
        lesson = db.lessons.find_one({'difficulty': 1}, {'_id': 0, 'id': 1})
    else:
        avg_score = sum(p['score'] for p in progress) / len(progress)
        difficulty = 1 if avg_score < 60 else 2  # Simple rule-based adaptation
        lesson = db.lessons.find_one(
            {'difficulty': difficulty, 'id': {'$nin': [p['lesson_id'] for p in progress]}},
            {'_id': 0, 'id': 1}
        )
    
    return lesson['id']
