from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

model = YOLO("best.pt")  # Load a pretrained YOLOv11 model

image = "13.jpg"  # change this to the path of image to run object detection on


# Predict on an image, show the results, save the output, and set confidence threshold to 0.1
model.predict(source=image, show=True, save=True, conf=0.1)

# Dynamically find the latest prediction folder
runs_dir = "runs/detect"
latest_folder = max([os.path.join(runs_dir, d) for d in os.listdir(runs_dir)], key=os.path.getmtime)

# Construct the path to the saved image
output_image_path = os.path.join(latest_folder, image)

# Open and display the saved image
img = mpimg.imread(output_image_path)
plt.imshow(img)
plt.axis('off')  # Turn off axis
plt.show()  # Keep the image open until manually closed