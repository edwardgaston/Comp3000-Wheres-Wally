import cv2
import numpy as np
import os
import random

# Paths to datasets
neg_path = "negatives/"
pos_path = "positives/"
output_images_path = "augmented_dataset/images/"
output_labels_path = "augmented_dataset/labels/"

# Ensure output paths exist
os.makedirs(output_images_path, exist_ok=True)
os.makedirs(output_labels_path, exist_ok=True)

# List all negative and positive images
neg_images = [os.path.join(neg_path, f) for f in os.listdir(neg_path) if f.endswith(('.jpg', '.png'))]
pos_images = [os.path.join(pos_path, f) for f in os.listdir(pos_path) if f.endswith(('.jpg', '.png'))]

# Transparency factor (0 = fully transparent, 1 = fully opaque)
ALPHA = 0.9  # Adjust as needed for slight transparency

# Function to overlay an object onto a background with transparency
def overlay_image(background, foreground):
    bg_h, bg_w, _ = background.shape
    fg_h, fg_w, _ = foreground.shape

    # Resize the positive image to fit within the negative image
    scale = min(bg_w / fg_w, bg_h / fg_h) * random.uniform(0.8, 0.9)  # Increased scale factor range
    new_w, new_h = int(fg_w * scale), int(fg_h * scale)
    foreground = cv2.resize(foreground, (new_w, new_h))

    # Random position within the negative image
    x_offset = random.randint(0, bg_w - new_w)
    y_offset = random.randint(0, bg_h - new_h)

    # Extract region from background where the positive image will be placed
    roi = background[y_offset:y_offset+new_h, x_offset:x_offset+new_w]

    # Convert foreground to grayscale to create a mask
    foreground_gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(foreground_gray, 1, 255, cv2.THRESH_BINARY)

    # Convert mask to 3 channels
    mask_3ch = cv2.merge([mask, mask, mask])

    # Apply transparency: Blend the positive image with the background
    blended = cv2.addWeighted(roi, 1 - ALPHA, foreground, ALPHA, 0)

    # Use the mask to only apply the blended region
    roi = np.where(mask_3ch == 255, blended, roi)

    # Put the modified ROI back into the background
    background[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = roi

    # Return the updated background and bounding box in YOLO format
    x_center = (x_offset + new_w / 2) / bg_w
    y_center = (y_offset + new_h / 2) / bg_h
    width = new_w / bg_w
    height = new_h / bg_h

    return background, (x_center, y_center, width, height)

# Generate dataset
for i, neg_img_path in enumerate(neg_images):
    background = cv2.imread(neg_img_path)
    
    pos_img_path = random.choice(pos_images)
    foreground = cv2.imread(pos_img_path, cv2.IMREAD_UNCHANGED)  # Load with transparency

    merged_img, bbox = overlay_image(background, foreground)

    # Save image and annotation
    cv2.imwrite(f"{output_images_path}/image_{i}.jpg", merged_img)
    with open(f"{output_labels_path}/image_{i}.txt", "w") as f:
        x_center, y_center, width, height = bbox
        f.write(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")  # YOLO format

print("Dataset augmentation complete!")