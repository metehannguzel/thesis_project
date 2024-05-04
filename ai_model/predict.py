from ultralytics import YOLO
from PIL import Image   
import os

model_path = os.path.join("runs/detect/train/weights/best.pt")

model = YOLO(model_path)

for i in range(0,11):

    img = Image.open(f"unseen_data/test_{i}.jpg")

    result = model.predict(source=img, save=True)