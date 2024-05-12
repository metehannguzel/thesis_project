from datetime import timedelta
import datetime
import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import cv2
from ultralytics import YOLO
import os
from io import BytesIO
import csv
import pandas as pd
import shutil
import json

class_dict = {0: "drinks", 1: "healthcare", 2: "personal", 3: "cleaning", 4: "glassware", 5: "food"}

relationship_scores = {
    "drinks": {"drinks": 1, "healthcare": 0.1, "personal": 0.2, "cleaning": 0.1, "glassware": 0.9, "food": 0.5},
    "healthcare": {"drinks": 0.1, "healthcare": 1, "personal": 0.8, "cleaning": 0.5, "glassware": 0.2, "food": 0.4},
    "personal": {"drinks": 0.2, "healthcare": 0.8, "personal": 1, "cleaning": 0.6, "glassware": 0.3, "food": 0.5},
    "cleaning": {"drinks": 0.1, "healthcare": 0.5, "personal": 0.6, "cleaning": 1, "glassware": 0.2, "food": 0.3},
    "glassware": {"drinks": 0.9, "healthcare": 0.2, "personal": 0.3, "cleaning": 0.2, "glassware": 1, "food": 0.4},
    "food": {"drinks": 0.5, "healthcare": 0.4, "personal": 0.5, "cleaning": 0.3, "glassware": 0.4, "food": 1}
}

def initialize_firebase():
    cred = credentials.Certificate("config_files/key.json")
    app = firebase_admin.initialize_app(cred, {"storageBucket": "thesisdemoproject.appspot.com"})

    return storage.bucket()

def load_latest_image(bucket):
    base_blobs = list(bucket.list_blobs(prefix="base/"))
    base_blobs.sort(key=lambda x: x.time_created, reverse=True)
    latest_blob = base_blobs[0]
    arr = np.frombuffer(latest_blob.download_as_string(), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    cv2.imshow("image", img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    return img, latest_blob.name

def predict_image(img, model_path):
    model = YOLO(model_path)

    return model(source=img, save_txt=True)

def process_predictions(file_path):
    with open(file_path, "r") as txt_file:
        with open("image0.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for line in txt_file:
                writer.writerow(line.strip().split(","))
    labels = pd.read_csv("image0.csv", header=None, sep="\s+")
    labels.columns = ["id", "x", "y", "width", "height"]

    return labels

def summarize_labels(labels, relationship_scores):
    id_counts = labels["id"].value_counts()
    most_common_id = id_counts.idxmax()
    category = class_dict.get(most_common_id, np.nan)

    outlier_ids = id_counts[id_counts.index != most_common_id]
    outlier_product_categories = [class_dict.get(id, np.nan) for id in outlier_ids.index]

    total_relationship_score = 0
    total_products = 0

    for outlier_id, count in outlier_ids.items():
        outlier_category = class_dict.get(outlier_id, np.nan)
        score = relationship_scores[category].get(outlier_category, 0)
        total_relationship_score += score * count
        total_products += count

    if total_products > 0:
        relationship_ratio = total_relationship_score / total_products
    else:
        relationship_ratio = 0

    product_count = id_counts[most_common_id]
    total_product_count = id_counts.sum()

    return category, outlier_product_categories, product_count, outlier_ids.sum(), total_product_count, relationship_ratio

def save_and_upload_result(results, file_name, bucket):
    for result in results:
        result.save(f"{file_name}")
    local_file_path = f"{file_name}"
    remote_file_path = f"predicted/{file_name}"

    return upload_to_firebase(local_file_path, remote_file_path, bucket)

def upload_to_firebase(local_file, remote_path, bucket):
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_file)
    url = blob.generate_signed_url(expiration=datetime.datetime.now() + timedelta(days=1))
    print(f"File uploaded to {remote_path}")
    
    return url

def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} successfully deleted.")
        else:
            print(f"{file_path} not found.")

def main():
    bucket = initialize_firebase()
    img, blob_name = load_latest_image(bucket)
    model_path = os.path.join("runs/detect/train/weights/best.pt")
    results = predict_image(img, model_path)
    labels = process_predictions("runs/detect/predict/labels/image0.txt")
    category, outlier_product_category, product_count, outlier_product_count, total_product_count, relationship_ratio = summarize_labels(labels, relationship_scores)
    file_name = os.path.basename(blob_name).split(".")[0] + "_predicted.jpg"
    rendered_image_url = save_and_upload_result(results, file_name, bucket)

    results_dict = {
    "category": str(category) if pd.notna(category) else "Empty",
    "outlier_product_category": ", ".join([str(cat) for cat in outlier_product_category if pd.notna(cat)]) if outlier_product_category else "Empty", #str([str(cat) for cat in outlier_product_category if pd.notna(cat)] if outlier_product_category else "Empty"),
    "product_count": int(product_count) if pd.notna(product_count) else -1,
    "outlier_product_count": int(outlier_product_count) if pd.notna(outlier_product_count) else -1,
    "total_product_count": int(total_product_count) if pd.notna(total_product_count) else -1,
    "relationship_ratio": round(float(relationship_ratio), 2) if pd.notna(relationship_ratio) else -1.0,
    "rendered_image_url": str(rendered_image_url) if rendered_image_url else "Empty"
    }
    
    print(json.dumps(results_dict))
    shutil.rmtree("runs/detect/predict")
    csv_file_path = "image0.csv"
    local_file_path = f"{file_name}"
    delete_files([csv_file_path, local_file_path])

if __name__ == "__main__":
    main()
