import React from 'react';

const DetectionResult = ({ result }) => {
  if (!result) return null;

  return (
    <div className="result">
      <h2>Detection Result</h2>
      {result.annotatedImageUrl && (
        <img src={result.annotatedImageUrl} alt="Detection Result" style={{ width: '100%' }} />
      )}
      {/* Or show bounding boxes info here */}
    </div>
  );
};

export default DetectionResult;
