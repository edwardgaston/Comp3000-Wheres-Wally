from ultralytics import YOLO

model = YOLO("best.pt")  # Load a pretrained YOLOv8 model

model.predict(source = "17.jpg", show=True, save=True, conf=0.1 )  # Predict on an image, show the results, save the output, and set confidence threshold to 0.3\an