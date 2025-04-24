import React, { useState } from 'react';
import { Box, Button, Typography, TextField, CircularProgress } from '@mui/material';
import axios from 'axios';

function UploadForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewImage(URL.createObjectURL(file)); // Create a preview URL for the uploaded image
      setError('');
      setProcessedImage(null); // Reset the processed image
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    setLoading(true); // Show the loading spinner
    setPreviewImage(null); // Hide the preview image

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
      const { processed_image_url } = resultsResponse.data;

      console.log('Processed Image URL:', processed_image_url);

      // Construct the full URL for the processed image
      const fullImageUrl = `http://localhost:5001${processed_image_url}`;
      console.log('Full Processed Image URL:', fullImageUrl);

      setProcessedImage(fullImageUrl); // Show the processed image
      setError('');
    } catch (err) {
      console.error('Error uploading image:', err.response || err.message);
      setError('Failed to process the image. Please try again.');
    } finally {
      setLoading(false); // Hide the loading spinner
    }
  };

  return (
    <Box sx={{ textAlign: 'center', marginTop: 4 }}>
      <Typography variant="h5" gutterBottom>
        Upload an Image to Find Wally
      </Typography>
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2 }}>
        <TextField
          type="file"
          onChange={handleFileChange}
          inputProps={{ accept: 'image/*' }}
          sx={{ marginBottom: 2, height: '56px' }} // Set height explicitly
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          sx={{ marginBottom: 2, height: '56px' }} // Match the height of the TextField
        >
          Find Wally
        </Button>
      </Box>
      {error && <Typography color="error">{error}</Typography>}

      {/* Show the preview image */}
      {previewImage && !processedImage && !loading && (
        <Box sx={{ marginTop: 4 }}>
          <Typography variant="h6">Preview Image:</Typography>
          <img
            src={previewImage}
            alt="Preview"
            style={{
              maxWidth: '90vw', // Limit width to 90% of the viewport width
              maxHeight: '80vh', // Limit height to 80% of the viewport height
              marginTop: 10,
              objectFit: 'contain', // Ensure the image maintains its aspect ratio
            }}
          />
        </Box>
      )}

      {/* Show the loading spinner */}
      {loading && (
        <Box sx={{ marginTop: 4 }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ marginTop: 2 }}>
            Processing the image...
          </Typography>
        </Box>
      )}

      {/* Show the processed image */}
      {processedImage && (
        <Box sx={{ marginTop: 4 }}>
          <Typography variant="h6">Processed Image:</Typography>
          <img
            src={processedImage}
            alt="Processed"
            style={{
              maxWidth: '90vw', // Limit width to 90% of the viewport width
              maxHeight: '80vh', // Limit height to 80% of the viewport height
              marginTop: 10,
              objectFit: 'contain', // Ensure the image maintains its aspect ratio
            }}
          />
        </Box>
      )}
    </Box>
  );
}

export default UploadForm;