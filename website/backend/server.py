from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw
from io import BytesIO
from ultralytics import YOLO  # Import YOLO model from ultralytics
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import uuid
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

#enable CORS for the app
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Connect to MongoDB using the URI from the .env file
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file")

client = MongoClient(MONGO_URI)
db = client['wheres_wally']
scans_collection = db['scans']

# Load your YOLO model
try:
    model = YOLO('best.pt')  # Load the YOLO model directly
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    # Load the image
    image_file = request.files['image']
    image = Image.open(image_file.stream).convert('RGB')

    # Perform inference
    results = model.predict(source=image, save=False)  # Use YOLO's predict method

    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    detections = []  # Store detection details for logging
    for box in results[0].boxes:
        bbox = box.xyxy.tolist()  # Bounding box coordinates
        if isinstance(bbox[0], list):  # Flatten the bbox if it's nested
            bbox = bbox[0]
        class_id = int(box.cls.item())  # Class index
        confidence = box.conf.item()  # Confidence score

        # Log detection details
        detections.append({
            "class": class_id,
            "confidence": confidence,
            "bbox": bbox
        })

        # Draw the bounding box
        draw.rectangle(bbox, outline="red", width=3)
        draw.text((bbox[0], bbox[1] - 10), f"Class: {class_id}, Conf: {confidence:.2f}", fill="red")

    # Save the processed image to a BytesIO object
    img_io = BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    image_data = img_io.getvalue()

    # Generate a unique ID for the scan
    scan_id = str(uuid.uuid4())

    # Save the results in MongoDB
    scans_collection.insert_one({
        "_id": scan_id,
        "detections": detections,
        "processed_image": image_data
    })

    # Return the scan ID to the frontend
    return jsonify({"scan_id": scan_id})

@app.route('/results/<scan_id>', methods=['GET'])
def get_results(scan_id):
    # Retrieve the scan results from MongoDB
    scan = scans_collection.find_one({"_id": scan_id})
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    # Return the detections and processed image URL
    return jsonify({
        "detections": scan["detections"],
        "processed_image_url": f"/processed_image/{scan_id}"
    })

@app.route('/processed_image/<scan_id>', methods=['GET'])
def get_processed_image(scan_id):
    # Retrieve the processed image from MongoDB
    scan = scans_collection.find_one({"_id": scan_id})
    if not scan:
        return jsonify({"error": "Image not found"}), 404

    # Return the image as a binary response
    img_io = BytesIO(scan["processed_image"])
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='localhost', port=5001)