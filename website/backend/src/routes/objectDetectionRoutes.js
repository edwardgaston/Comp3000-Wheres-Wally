const express = require('express');
const ObjectDetectionController = require('../controllers/objectDetectionController');

const router = express.Router();
const objectDetectionController = new ObjectDetectionController();

router.post('/detections', objectDetectionController.createDetection.bind(objectDetectionController));
router.get('/detections', objectDetectionController.getDetections.bind(objectDetectionController));

module.exports = router;