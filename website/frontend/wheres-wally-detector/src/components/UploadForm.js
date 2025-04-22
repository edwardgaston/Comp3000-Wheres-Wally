import React, { useState } from 'react';
import { Box, Button, Typography, TextField } from '@mui/material';
import axios from 'axios';

function UploadForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [detections, setDetections] = useState([]);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setError('');
    setProcessedImage(null); // Reset the processed image
    setDetections([]); // Reset detections
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      // Send the image to the backend
      const response = await axios.post('http://localhost:5001/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { scan_id } = response.data;
      console.log('Scan ID:', scan_id);

      // Fetch the results using the scan ID
      const resultsResponse = await axios.get(`http://localhost:5001/results/${scan_id}`);
      const { detections, processed_image_url } = resultsResponse.data;

      console.log('Detections:', detections);
      console.log('Processed Image URL:', processed_image_url);

      // Construct the full URL for the processed image
      const fullImageUrl = `http://localhost:5001${processed_image_url}`;
      console.log('Full Processed Image URL:', fullImageUrl);

      setDetections(detections);
      setProcessedImage(fullImageUrl);
      setError('');
    } catch (err) {
      console.error('Error uploading image:', err.response || err.message);
      setError('Failed to process the image. Please try again.');
    }
  };

  return (
    <Box sx={{ textAlign: 'center', marginTop: 4 }}>
      <Typography variant="h5" gutterBottom>
        Upload an Image to Find Wally
      </Typography>
      <TextField
        type="file"
        onChange={handleFileChange}
        inputProps={{ accept: 'image/*' }}
        sx={{ marginBottom: 2 }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        sx={{ marginBottom: 2 }}
      >
        Find Wally
      </Button>
      {error && <Typography color="error">{error}</Typography>}
      {detections.length > 0 && (
        <Box sx={{ marginTop: 4 }}>
          <Typography variant="h6">Detections:</Typography>
          <pre>{JSON.stringify(detections, null, 2)}</pre>
        </Box>
      )}
      {processedImage && (
        <Box sx={{ marginTop: 4 }}>
          <Typography variant="h6">Processed Image:</Typography>
          <img src={processedImage} alt="Processed" style={{ maxWidth: '100%', marginTop: 10 }} />
        </Box>
      )}
    </Box>
  );
}

export default UploadForm;