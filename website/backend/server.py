from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from ultralytics import YOLO
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import uuid
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the app
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
    results = model.predict(source=image, save=False)

    # Define colors for bounding boxes (one for each class)
    colors = {
        0: "red",       # Odlaw
        1: "orange",    # Wally
        2: "navy",      # Wenda
        3: "green",     # Wizard
        4: "yellow",    # Woof
    }

    # Define character names for each class
    character_names = {
        0: "Odlaw",
        1: "Wally",
        2: "Wenda",
        3: "Wizard",
        4: "Woof",
    }

    # Load a larger font for the labels
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Use Arial font with size 20
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if Arial is unavailable

    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    detections = []  # Store detection details for logging
    for box in results[0].boxes:
        bbox = box.xyxy.tolist()  # Bounding box coordinates
        if isinstance(bbox[0], list):  # Flatten the bbox if it's nested
            bbox = bbox[0]
        class_id = int(box.cls.item())  # Class index
        confidence = box.conf.item()  # Confidence score

        # Get the color for the class (default to black if class is not in colors)
        color = colors.get(class_id, "black")

        # Get the character name for the class
        character_name = character_names.get(class_id, f"Class {class_id}")

        # Log detection details
        detections.append({
            "class": class_id,
            "character": character_name,
            "confidence": confidence,
            "bbox": bbox
        })

        # Draw the bounding box with a thin black outline and a thicker colored box
        draw.rectangle(
            [bbox[0] - 1, bbox[1] - 1, bbox[2] + 1, bbox[3] + 1],
            outline="black",  # Thin black outline
            width=2
        )
        draw.rectangle(
            [bbox[0], bbox[1], bbox[2], bbox[3]],
            outline=color,
            width=5  # Main bounding box
        )

        # Add a label above the bounding box
        label = f"{character_name}, Conf: {confidence:.2f}"
        text_bbox = draw.textbbox((bbox[0], bbox[1]), label, font=font)  # Get the bounding box of the text
        text_width = text_bbox[2] - text_bbox[0]  # Calculate text width
        text_height = text_bbox[3] - text_bbox[1]  # Calculate text height
        padding = 5  # Add padding around the label
        text_position = (bbox[0], bbox[1] - text_height - padding - 5)  # Position above the box

        # Draw a rectangle as the background for the label with a black outline
        draw.rectangle(
            [
                text_position[0] - padding - 1,
                text_position[1] - padding - 1,
                text_position[0] + text_width + padding + 1,
                text_position[1] + text_height + padding + 1,
            ],
            outline="black",  # Thin black outline
            width=2
        )
        draw.rectangle(
            [
                text_position[0] - padding,
                text_position[1] - padding,
                text_position[0] + text_width + padding,
                text_position[1] + text_height + padding,
            ],
            fill=color  # Background for the label
        )

        # Draw the label text
        draw.text(text_position, label, fill="white", font=font)

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