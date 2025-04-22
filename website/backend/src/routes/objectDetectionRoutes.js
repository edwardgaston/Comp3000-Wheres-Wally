import express from 'express';
import multer from 'multer';
import axios from 'axios';
import FormData from 'form-data'; // Import FormData for multipart/form-data
import ObjectDetectionController from '../controllers/objectDetectionController.js';

const router = express.Router();
const objectDetectionController = new ObjectDetectionController();
const upload = multer(); // Initialize multer for handling file uploads

// Route to handle object detection using the Python server
router.post('/detect', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No image uploaded' });
        }

        // Create a FormData object to send the image as multipart/form-data
        const formData = new FormData();
        formData.append('image', req.file.buffer, req.file.originalname);

        // Send the image to the Python server
        const response = await axios.post('http://localhost:5001/detect', formData, {
            headers: {
                ...formData.getHeaders(), // Include the correct headers for multipart/form-data
            },
        });

        // Return the detection results from the Python server to the frontend
        res.status(200).json(response.data);
    } catch (error) {
        console.error('Error communicating with Python server:', error.message);
        res.status(500).json({ error: 'Error processing detection', details: error.message });
    }
});

// Existing routes for database operations
router.post('/detections', objectDetectionController.createDetection.bind(objectDetectionController));
router.get('/detections', objectDetectionController.getDetections.bind(objectDetectionController));

export default router;