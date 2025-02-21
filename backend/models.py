from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def init_db():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['learning_path']
        
        # Drop existing collections if they exist
        for collection_name in ['students', 'careers', 'lessons', 'progress']:
            if collection_name in db.list_collection_names():
                db.drop_collection(collection_name)
        
        # Create collections with validation schemas
        db.create_collection('students', validator={

            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['name', 'interests', 'skills'],
                'properties': {
                    'name': {'bsonType': 'string'},
                    'interests': {'bsonType': 'array'},
                    'skills': {'bsonType': 'array'}
                }
            }
        })
        
        db.create_collection('careers', validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['name', 'required_skills', 'description'],
                'properties': {
                    'name': {'bsonType': 'string'},
                    'required_skills': {'bsonType': 'array'},
                    'description': {'bsonType': 'string'}
                }
            }
        })
        
        db.create_collection('lessons', validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['title', 'difficulty', 'content'],
                'properties': {
                    'title': {'bsonType': 'string'},
                    'difficulty': {'bsonType': 'int'},
                    'content': {'bsonType': 'string'}
                }
            }
        })
        
        db.create_collection('progress', validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['student_id', 'lesson_id', 'score', 'completed'],
                'properties': {
                    'student_id': {'bsonType': 'int'},
                    'lesson_id': {'bsonType': 'int'},
                    'score': {'bsonType': 'int'},
                    'completed': {'bsonType': 'bool'}
                }
            }
        })
        
        # Insert sample data if collections are empty
        if db.careers.count_documents({}) == 0:
            db.careers.insert_many([
                {
                    'name': 'Engineer',
                    'required_skills': ['math', 'science'],
                    'description': 'Builds stuff'
                },
                {
                    'name': 'Artist',
                    'required_skills': ['art', 'creativity'],
                    'description': 'Creates art'
                }
            ])
            
        if db.lessons.count_documents({}) == 0:
            db.lessons.insert_many([
                {
                    'title': 'Basic Math',
                    'difficulty': 1,
                    'content': 'Learn addition'
                },
                {
                    'title': 'Algebra',
                    'difficulty': 2,
                    'content': 'Solve equations'
                }
            ])
            
        return db
        
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

if __name__ == "__main__":
    db = init_db()
    # Create indexes after initialization
    db.students.create_index('id', unique=True)
    db.careers.create_index('id', unique=True)
    db.lessons.create_index('id', unique=True)
    db.progress.create_index([('student_id', 1), ('lesson_id', 1)], unique=True)
