import cv2
import os
import numpy as np

# Paths
positive_image_path = 'positives/wally.jpg'
negatives_file = 'updated_negatives.txt'
output_vec_file = 'positives.vec'
num_samples = 2000

# Read negative images paths
with open(negatives_file, 'r') as file:
    negative_images = [line.strip() for line in file.readlines() if line.strip()]

# Debugging output: Print the first few paths to verify
print("First few negative image paths:")
for path in negative_images[:5]:
    print(path)

# Load the positive image
positive_image = cv2.imread(positive_image_path, cv2.IMREAD_UNCHANGED)
if positive_image is None:
    raise FileNotFoundError(f"Positive image not found: {positive_image_path}")

positive_height, positive_width = positive_image.shape[:2]

# Create samples
samples = []
for i in range(num_samples):
    # Randomly select a negative image
    negative_image_path = np.random.choice(negative_images).strip()
    
    # Debugging output
    print(f"Attempting to read negative image: '{negative_image_path}'")
    
    # Check if the file exists
    if not os.path.isfile(negative_image_path):
        print(f"File does not exist: '{negative_image_path}'")
        continue
    
    negative_image = cv2.imread(negative_image_path)

    if negative_image is None:
        print(f"Warning: Negative image not found or cannot be read: '{negative_image_path}'")
        continue

    # Debugging output
    print(f"Processing negative image: '{negative_image_path}'")

    # Randomly select a position to overlay the positive image
    x_offset = np.random.randint(0, negative_image.shape[1] - positive_width)
    y_offset = np.random.randint(0, negative_image.shape[0] - positive_height)

    # Overlay the positive image onto the negative image
    sample = negative_image.copy()
    sample[y_offset:y_offset+positive_height, x_offset:x_offset+positive_width] = positive_image

    # Save the sample
    sample_path = f'samples/sample_{i}.jpg'
    cv2.imwrite(sample_path, sample)
    samples.append(sample_path)

# Save the samples to the .vec file
with open(output_vec_file, 'w') as file:
    for sample in samples:
        file.write(f'{sample}\n')