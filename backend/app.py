# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from recommendations import recommend_career, recommend_next_lesson
from rl_progress import update_progress
from models import init_db

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['learning_path']


app = Flask(__name__)
CORS(app)


@app.route('/api/recommend-career', methods=['POST'])
def career_endpoint():
    try:
        data = request.get_json()
        if not data or 'interests' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        career = recommend_career(data['interests'])
        return jsonify({'career': career})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/next-lesson', methods=['POST'])
def lesson_endpoint():
    try:
        data = request.get_json()
        if not data or 'student_id' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        lesson_id = recommend_next_lesson(data['student_id'])
        lesson = db.lessons.find_one({'id': lesson_id}, {'_id': 0, 'title': 1, 'content': 1})
        
        if not lesson:
            return jsonify({'error': 'Lesson not found'}), 404

            
        return jsonify({
            'lesson_id': lesson_id,
            'title': lesson['title'],
            'content': lesson['content']
        })

    except PyMongoError as e:
        return jsonify({'error': f'MongoDB error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/update-progress', methods=['POST'])
def progress_endpoint():
    try:
        data = request.get_json()
        if not data or 'student_id' not in data or 'lesson_id' not in data or 'score' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        update_progress(data['student_id'], data['lesson_id'], data['score'])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Initialize database
    db = init_db()
    
    # Drop existing collections to start fresh
    db.students.drop()
    db.careers.drop()
    db.lessons.drop()
    db.progress.drop()
    
    # Reinitialize collections with proper indexes
    init_db()
    
    # Create indexes after ensuring all documents have required fields
    try:
        # Ensure all documents have an 'id' field
        db.students.update_many({'id': {'$exists': False}}, [{'$set': {'id': {'$toString': '$_id'}}}])
        db.careers.update_many({'id': {'$exists': False}}, [{'$set': {'id': {'$toString': '$_id'}}}])
        db.lessons.update_many({'id': {'$exists': False}}, [{'$set': {'id': {'$toString': '$_id'}}}])
        
        # Create indexes
        db.students.create_index('id', unique=True)
        db.careers.create_index('id', unique=True)
        db.lessons.create_index('id', unique=True)
        db.progress.create_index([('student_id', 1), ('lesson_id', 1)], unique=True)
    except Exception as e:
        print(f"Error creating indexes: {e}")

    
    app.run(debug=True)
