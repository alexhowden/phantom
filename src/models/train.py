from ultralytics import YOLO

model = YOLO('./yolo_models/yolo11s.pt')

model.train(data='dataset_state.yaml', imgsz=640, batch=8, epochs=100, workers=0, device='cpu')
