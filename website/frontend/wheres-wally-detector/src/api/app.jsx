import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import DetectionResult from './components/DetectionResult';

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="App">
      <h1>Where's Wally Detector</h1>
      <UploadForm onResult={setResult} />
      <DetectionResult result={result} />
    </div>
  );
}

export default App;
