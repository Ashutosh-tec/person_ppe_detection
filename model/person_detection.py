from ultralytics import YOLO

# load model
model = YOLO("yolov8n.pt")

# train
results = model.train(data="config.yaml", epochs = 5, batch = 4)

