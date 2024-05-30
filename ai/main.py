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

# Define class categories
class_dict = {0: "drinks", 1: "healthcare", 2: "personal", 3: "cleaning", 4: "glassware", 5: "food"}

# Define relationship scores between different categories
relationship_scores = {
    "drinks": {"drinks": 1, "healthcare": 0.1, "personal": 0.2, "cleaning": 0.1, "glassware": 0.9, "food": 0.5},
    "healthcare": {"drinks": 0.1, "healthcare": 1, "personal": 0.8, "cleaning": 0.5, "glassware": 0.2, "food": 0.4},
    "personal": {"drinks": 0.2, "healthcare": 0.8, "personal": 1, "cleaning": 0.6, "glassware": 0.3, "food": 0.5},
    "cleaning": {"drinks": 0.1, "healthcare": 0.5, "personal": 0.6, "cleaning": 1, "glassware": 0.2, "food": 0.3},
    "glassware": {"drinks": 0.9, "healthcare": 0.2, "personal": 0.3, "cleaning": 0.2, "glassware": 1, "food": 0.4},
    "food": {"drinks": 0.5, "healthcare": 0.4, "personal": 0.5, "cleaning": 0.3, "glassware": 0.4, "food": 1}
}

# Initialize Firebase connection
def initialize_firebase():
    cred = credentials.Certificate("config_files/key.json")                                         # Load Firebase credentials
    app = firebase_admin.initialize_app(cred, {"storageBucket": "thesisdemoproject.appspot.com"})   # Initialize Firebase app

    return storage.bucket()                                                                         # Return the storage bucket

# Load the latest image from Firebase storage                       
def load_latest_image(bucket):                      
    base_blobs = list(bucket.list_blobs(prefix="base/"))            # List all blobs in the 'base' directory
    base_blobs.sort(key=lambda x: x.time_created, reverse=True)     # Sort blobs by creation time, latest first
    latest_blob = base_blobs[0]                                     # Get the latest blob
    arr = np.frombuffer(latest_blob.download_as_string(), np.uint8) # Download the image as a numpy array
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)                       # Decode the image
    cv2.imshow("image", img)                                        # Display the image
    cv2.waitKey(1000)                                               # Wait for 1 second
    cv2.destroyAllWindows()                                         # Close the image window

    return img, latest_blob.name                                    # Return the image and its name

# Predict objects in the image using the YOLO model                     
def predict_image(img, model_path):                     
    model = YOLO(model_path)                # Load the YOLO model

    return model(source=img, save_txt=True) # Predict objects and save results as text

# Process prediction results from a text file to a CSV format                       
def process_predictions(file_path):                     
    with open(file_path, "r") as txt_file:                      
        with open("image0.csv", "w", newline="") as csv_file:                       
            writer = csv.writer(csv_file)                       
            for line in txt_file:                       
                writer.writerow(line.strip().split(","))        # Write each line from the text file to the CSV
    labels = pd.read_csv("image0.csv", header=None, sep="\s+")  # Read the CSV file into a pandas DataFrame
    labels.columns = ["id", "x", "y", "width", "height"]        # Set the column names

    return labels                                               # Return the labels DataFrame

# Summarize the prediction results                      
def summarize_labels(labels, relationship_scores):                      
    id_counts = labels["id"].value_counts()                                                                                 # Count occurrences of each ID
    most_common_id = id_counts.idxmax()                                                                                     # Get the most common ID
    category = class_dict.get(most_common_id, np.nan)                                                                       # Get the category of the most common ID

    outlier_ids = id_counts[id_counts.index != most_common_id]                                                              # Get IDs that are not the most common
    outlier_product_categories = [class_dict.get(id, np.nan) for id in outlier_ids.index]                                   # Get their categories

    total_relationship_score = 0
    total_products = 0

    for outlier_id, count in outlier_ids.items():
        outlier_category = class_dict.get(outlier_id, np.nan)                                                               # Get the category of the outlier ID
        score = relationship_scores[category].get(outlier_category, 0)                                                      # Get the relationship score
        total_relationship_score += score * count                                                                           # Calculate the total relationship score
        total_products += count                                                                                             # Calculate the total number of products

    if total_products > 0:                      
        relationship_ratio = total_relationship_score / total_products                                                      # Calculate the relationship ratio
    else:
        relationship_ratio = 0

    product_count = id_counts[most_common_id]                                                                               # Count of the most common product
    total_product_count = id_counts.sum()                                                                                   # Total number of products

    return category, outlier_product_categories, product_count, outlier_ids.sum(), total_product_count, relationship_ratio  # Return the summary

# Save and upload the prediction result image to Firebase
def save_and_upload_result(results, file_name, bucket):
    for result in results:
        result.save(f"{file_name}")                                         # Save the prediction result
    local_file_path = f"{file_name}"                                        # Local path of the saved file
    remote_file_path = f"predicted/{file_name}"                             # Remote path for Firebase upload

    return upload_to_firebase(local_file_path, remote_file_path, bucket)    # Upload the file to Firebase

# Upload a file to Firebase storage
def upload_to_firebase(local_file, remote_path, bucket):
    blob = bucket.blob(remote_path)                                                         # Create a blob in Firebase storage
    blob.upload_from_filename(local_file)                                                   # Upload the local file
    url = blob.generate_signed_url(expiration=datetime.datetime.now() + timedelta(days=1))  # Generate a signed URL
    print(f"File uploaded to {remote_path}")                                                # Print confirmation
    
    return url                                                                              # Return the URL

# Delete local files
def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)                        # Remove the file
            print(f"{file_path} successfully deleted.") # Print confirmation
        else:
            print(f"{file_path} not found.")            # Print if the file was not found

# Main function to orchestrate the process
def main():
    bucket = initialize_firebase()                                                                                                                                      # Initialize Firebase
    img, blob_name = load_latest_image(bucket)                                                                                                                          # Load the latest image
    model_path = os.path.join("runs/detect/train/weights/best.pt")                                                                                                      # Path to the YOLO model
    results = predict_image(img, model_path)                                                                                                                            # Predict objects in the image
    labels = process_predictions("runs/detect/predict/labels/image0.txt")                                                                                               # Process the prediction results
    category, outlier_product_category, product_count, outlier_product_count, total_product_count, relationship_ratio = summarize_labels(labels, relationship_scores)   # Summarize the results
    file_name = os.path.basename(blob_name).split(".")[0] + "_predicted.jpg"                                                                                            # Create a name for the prediction result file
    rendered_image_url = save_and_upload_result(results, file_name, bucket)                                                                                             # Save and upload the result

    results_dict = {
    "category": str(category) if pd.notna(category) else "Empty",                                                                                                       # Handle category
    "outlier_product_category": ", ".join([str(cat) for cat in outlier_product_category if pd.notna(cat)]) if outlier_product_category else "Empty",                    # Handle outlier categories
    "product_count": int(product_count) if pd.notna(product_count) else -1,                                                                                             # Handle product count
    "outlier_product_count": int(outlier_product_count) if pd.notna(outlier_product_count) else -1,                                                                     # Handle outlier product count
    "total_product_count": int(total_product_count) if pd.notna(total_product_count) else -1,                                                                           # Handle total product count
    "relationship_ratio": float(relationship_ratio) if pd.notna(relationship_ratio) else -1.0,                                                                          # Handle relationship ratio
    "rendered_image_url": str(rendered_image_url) if rendered_image_url else "Empty"                                                                                    # Handle rendered image URL
    }
    
    print(json.dumps(results_dict))                                                                                                                                     # Print the results as JSON
    shutil.rmtree("runs/detect/predict")                                                                                                                                # Remove the prediction directory
    csv_file_path = "image0.csv"                                                                                                                                        # Path to the CSV file
    local_file_path = f"{file_name}"                                                                                                                                    # Path to the local file
    delete_files([csv_file_path, local_file_path])                                                                                                                      # Delete the local files


if __name__ == "__main__":
    main()                                                                                                                                                              # Run the main function

