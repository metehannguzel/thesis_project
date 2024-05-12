import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, jsonify, request
import numpy as np
import cv2
from ultralytics import YOLO
import os

app = Flask(__name__)

model_path = os.path.join("runs/detect/train/weights/best.pt")
model = YOLO(model_path)

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"storageBucket": "thesisdemoproject.appspot.com"})
bucket = storage.bucket()

def upload_to_firebase(local_file, remote_path):
    bucket = storage.bucket()
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_file)
    print(f"File uploaded to {remote_path}")

@app.route("/") 
def hello(): 
    return "Hello, World!" 

@app.route("/process_image", methods=["GET"])
def process_image():
    try:
        base_blobs = list(bucket.list_blobs(prefix="base/"))
        base_blobs.sort(key=lambda x: x.time_created, reverse=True)
        latest_blob = base_blobs[0]
        file_name = os.path.basename(latest_blob.name).split('.')[0] + '_predicted.jpg'

        arr = np.frombuffer(latest_blob.download_as_string(), np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        cv2.imshow("image", img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

        results = model(source=img)

        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            obb = result.obb  # Oriented boxes object for OBB outputs
            result.save(f"predicted/{file_name}")

        local_file_path = f"predicted/{file_name}"
        remote_file_path = f"predicted/{file_name}"

        upload_to_firebase(local_file_path, remote_file_path)
        
        return jsonify({"message": "Image processed and uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
