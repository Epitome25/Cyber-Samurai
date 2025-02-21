// frontend/src/components/LessonViewer.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function LessonViewer({ studentId }) {
  const [lesson, setLesson] = useState(null);
  const [score, setScore] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);


  useEffect(() => {
    fetchLesson();
  }, []);

  const fetchLesson = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/api/next-lesson', { student_id: studentId });
      setLesson(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch lesson');
    } finally {
      setLoading(false);
    }
  };


  const handleSubmitScore = async () => {
    if (!score || isNaN(score) || score < 0 || score > 100) {
      setError('Please enter a valid score between 0 and 100');
      return;
    }
    
    try {
      await axios.post('http://localhost:5000/api/update-progress', {
        student_id: studentId,
        lesson_id: lesson.lesson_id,
        score: parseInt(score),
      });
      setScore('');
      fetchLesson();
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to update progress');
    }
  };



  return (
    <div>
      <h2>Lesson Viewer</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading ? (
        <p>Loading lesson...</p>
      ) : lesson ? (
        <>
          <p><strong>{lesson.title}</strong>: {lesson.content}</p>
          <div style={{ margin: '20px 0', display: 'flex', gap: '10px', alignItems: 'center' }}>
            <input
              type="number"
              value={score}
              onChange={(e) => setScore(e.target.value)}
              placeholder="Enter your score (0-100)"
              min="0"
              max="100"
              style={{
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '16px',
                width: '200px'
              }}
            />
            <button 
              onClick={handleSubmitScore}
              style={{
                padding: '8px 16px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '16px'
              }}
            >
              Submit Score
            </button>
          </div>

        </>
      ) : (
        <p>No lesson available</p>
      )}
    </div>
  );


}

export default LessonViewer;
