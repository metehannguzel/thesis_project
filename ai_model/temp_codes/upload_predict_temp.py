import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import cv2
from ultralytics import YOLO
from PIL import Image
import os
from io import BytesIO
import matplotlib.pyplot as plt
import csv
import pandas as pd
import shutil

class_dict = {0: "drinks", 1: "healthcare", 2: "personal", 3: "cleaning", 4: "glassware", 5: "food"}

model_path = os.path.join("runs/detect/train/weights/best.pt")
model = YOLO(model_path)

cred = credentials.Certificate("config_files/key.json")
app = firebase_admin.initialize_app(cred, {"storageBucket": "thesisdemoproject.appspot.com"})

bucket = storage.bucket()

base_blobs = list(bucket.list_blobs(prefix="base/"))
base_blobs.sort(key=lambda x: x.time_created, reverse=True)
latest_blob = base_blobs[0]
file_name = os.path.basename(latest_blob.name).split(".")[0] + "_predicted.jpg"

arr = np.frombuffer(latest_blob.download_as_string(), np.uint8)
img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
cv2.imshow("image", img)
cv2.waitKey(1000)
cv2.destroyAllWindows()

results = model(source=img, save_txt=True)

with open("runs/detect/predict/labels/image0.txt", "r") as txt_file:
    with open("image0.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        
        for line in txt_file:
            writer.writerow(line.strip().split(","))

shutil.rmtree("runs/detect/predict")
    

labels = pd.read_csv("image0.csv", header=None, sep="\s+")
labels.columns = ["id", "x", "y", "width", "height"]

id_counts = labels["id"].value_counts()
most_common_id = id_counts.idxmax()
least_common_id = id_counts.idxmin() if len(id_counts) > 1 else np.nan

category = class_dict.get(most_common_id, np.nan)
outlierProductCategory = class_dict.get(least_common_id, np.nan)
productCount = id_counts[most_common_id]
outlierProductCount = id_counts.get(least_common_id, np.nan)
totalProductCount = labels["id"].count()


for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.save(f"predicted/{file_name}")


def upload_to_firebase(local_file, remote_path):
    bucket = storage.bucket()
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_file)
    print(f"File uploaded to {remote_path}")

local_file_path = f"predicted/{file_name}"
remote_file_path = f"predicted/{file_name}"

upload_to_firebase(local_file_path, remote_file_path)




"""def main():
    bucket = initialize_firebase()
    img, blob_name = load_latest_image(bucket)
    model_path = os.path.join("runs/detect/train/weights/best.pt")
    results = predict_image(img, model_path)
    labels = process_predictions("runs/detect/predict/labels/image0.txt")
    category, outlier_product_category, product_count, outlier_product_count, total_product_count = summarize_labels(labels)
    file_name = os.path.basename(blob_name).split(".")[0] + "_predicted.jpg"
    rendered_image_url = save_and_upload_result(results, file_name, bucket)

    results_dict = {
    "category": str(category) if pd.notna(category) else "Empty",
    "outlier_product_category": str([str(cat) for cat in outlier_product_category if pd.notna(cat)] if outlier_product_category else ["Empty"]),
    "product_count": int(product_count) if pd.notna(product_count) else -1,
    "outlier_product_count": int(outlier_product_count) if pd.notna(outlier_product_count) else -1,
    "total_product_count": int(total_product_count) if pd.notna(total_product_count) else -1,
    "relationship_ratio": 0.90,
    "rendered_image_url": str(rendered_image_url) if rendered_image_url else "Empty"
    }
    
    print(json.dumps(results_dict))

    shutil.rmtree("runs/detect/predict")"""

####################################################################################################

"""def summarize_labels(labels):
    id_counts = labels["id"].value_counts()
    most_common_id = id_counts.idxmax()
    least_common_id = id_counts.idxmin() if len(id_counts) > 1 else np.nan
    category = class_dict.get(most_common_id, np.nan)
    outlierProductCategory = class_dict.get(least_common_id, np.nan)
    productCount = id_counts[most_common_id]
    outlierProductCount = id_counts.get(least_common_id, np.nan)
    totalProductCount = labels["id"].count()
    return category, outlierProductCategory, productCount, outlierProductCount, totalProductCount"""

"""results_dict = {
    "category": str(category) if pd.notna(category) else "Empty",
    "outlier_product_category": str(outlierProductCategory) if pd.notna(outlierProductCategory) else "Empty",
    "product_count": int(productCount) if pd.notna(productCount) else -1,
    "outlier_product_count": int(outlierProductCount) if pd.notna(outlierProductCount) else -1,
    "total_product_count": int(totalProductCount) if pd.notna(totalProductCount) else -1,
    "relationship_ratio": 0.90,
    "rendered_image_url": "AAAAAAA"#str(rendered_image_url) if pd.notna(totalProductCount) else "Empty"
    }"""



"""def summarize_labels(labels):
    id_counts = labels["id"].value_counts()
    most_common_id = id_counts.idxmax()
    category = class_dict.get(most_common_id, np.nan)
    
    product_count = id_counts[most_common_id]
    
    outlier_ids = id_counts[id_counts.index != most_common_id]
    outlier_product_categories = [class_dict.get(id, np.nan) for id in outlier_ids.index]
    outlier_product_count = outlier_ids.sum()
    total_product_count = id_counts.sum()
    
    return category, outlier_product_categories, product_count, outlier_product_count, total_product_count"""