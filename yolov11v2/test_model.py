import tensorflow as tf
import numpy as np
from PIL import Image, ImageDraw

# === Load the model ===
model = tf.saved_model.load("model_tf")
infer = model.signatures["serving_default"]

# === Load and preprocess image ===
image_path = "17.jpg"  # Make sure this image is in the same directory
img = Image.open(image_path).convert("RGB").resize((640, 640))
original_img = Image.open(image_path)  # To keep the original image for visualization

# Convert image to numpy array and normalize
img_array = np.array(img).astype(np.float32) / 255.0

# === Transpose to (batch_size, channels, height, width) ===
img_array = np.transpose(img_array, (2, 0, 1))  # Change from (640, 640, 3) to (3, 640, 640)

# === Add batch dimension and make tensor ===
img_tensor = tf.constant(img_array[np.newaxis, ...])  # [1, 3, 640, 640]

# === Run inference ===
output = infer(img_tensor)

# Print the keys of the output to check its structure
print(f"Output keys: {output.keys()}")

# Extract prediction details based on the correct key
for key, value in output.items():
    print(f"{key}: shape={value.shape}")
