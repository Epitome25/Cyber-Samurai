// frontend/src/components/CareerRecommendation.js
import React, { useState } from 'react';
import axios from 'axios';

function CareerRecommendation() {
  const [interests, setInterests] = useState('');
  const [career, setCareer] = useState('');

  const handleSubmit = async () => {
    const response = await axios.post('http://localhost:5000/api/recommend-career', { interests });
    setCareer(response.data.career);
  };

  return (
    <div>
      <h2>Career Recommendation</h2>
      <input 
        type="text" 
        value={interests} 
        onChange={(e) => setInterests(e.target.value)} 
        placeholder="e.g., math, art"
      />
      <button onClick={handleSubmit}>Recommend Career</button>
      {career && <p>Recommended Career: {career}</p>}
    </div>
  );
}

export default CareerRecommendation;