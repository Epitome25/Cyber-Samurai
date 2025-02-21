// frontend/src/App.js
import React from 'react';
import CareerRecommendation from './components/CareerRecommendation';
import LessonViewer from './components/LessonViewer';

function App() {
  return (
    <div className="App">
      <h1>Personalized Learning Path Generator</h1>
      <CareerRecommendation />
      <LessonViewer studentId={1} /> {/* Hardcoded for demo */}
    </div>
  );
}

export default App;
