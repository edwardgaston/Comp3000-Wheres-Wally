import torch
from ultralytics import YOLO

# Load your trained YOLOv11 model
model = YOLO("convert.pt")  # path to your best model
model = model.model  # Extract PyTorch model from Ultralytics wrapper
model.eval()

# Create dummy input with correct shape
dummy_input = torch.randn(1, 3, 640, 640)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    "yolov11.onnx",
    input_names=["images"],
    output_names=["output"],
    opset_version=11,
    export_params=True,
    do_constant_folding=True
)
