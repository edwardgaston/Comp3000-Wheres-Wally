const mongoose = require('mongoose');

const objectDetectionSchema = new mongoose.Schema({
    imageUrl: {
        type: String,
        required: true
    },
    detections: [
        {
            label: {
                type: String,
                required: true
            },
            confidence: {
                type: Number,
                required: true
            },
            boundingBox: {
                x: {
                    type: Number,
                    required: true
                },
                y: {
                    type: Number,
                    required: true
                },
                width: {
                    type: Number,
                    required: true
                },
                height: {
                    type: Number,
                    required: true
                }
            }
        }
    ]
});

module.exports = mongoose.model('ObjectDetection', objectDetectionSchema);