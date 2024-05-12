import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import cv2
from ultralytics import YOLO
from PIL import Image   
import os
import io


model_path = os.path.join("runs/detect/train/weights/best.pt")

model = YOLO(model_path)

img = Image.open(f"unseen_data/test_0.jpg")

result = model.predict(source=img, save=True, save_txt=True, save_conf=True)

for detection in result:
    bbox = detection[:4]  # x_min, y_min, x_max, y_max
    conf = detection[4]   # confidence
    class_id = int(detection[5])  # class id
    
    # bbox'u kullanarak PIL görüntüsünü kırpın
    cropped_img = img.crop(bbox)
    
    # Sonucu işleyin veya kaydedin
    cropped_img.show()