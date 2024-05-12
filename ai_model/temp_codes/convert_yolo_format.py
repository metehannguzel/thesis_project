import os
import pandas as pd

base_output_folder = "data/labels"

annotations = pd.read_csv("annotations/annotations_train_new_classes.csv")
class_names = annotations["class"].unique()
class_dict = {name: idx for idx, name in enumerate(class_names)}

for image_name, group in annotations.groupby("image_name"):
    txt_file_path = os.path.join(base_output_folder, image_name.replace(".jpg", ".txt"))
    with open(txt_file_path, "w") as f:
        for _, row in group.iterrows():
            x_center = ((row["x1"] + row["x2"]) / 2) / row["width"]
            y_center = ((row["y1"] + row["y2"]) / 2) / row["height"]
            bbox_width = (row["x2"] - row["x1"]) / row["width"]
            bbox_height = (row["y2"] - row["y1"]) / row["height"]
            
            class_id = class_dict[row["class"]]
            
            f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# {"drinks": 0, "healthcare": 1, "personal_care": 2, "home": 3, "food": 4, "pets": 5}

# {"drinks": 0, "healthcare": 1, "personal": 2, "cleaning": 3, "glassware": 4, "food": 5}

####################################################################################################

import pandas as pd
import os

# CSV dosyasını yükle
df = pd.read_csv("annotations/annotations_train_test_val_new_classes.csv")

class_names = df["class"].unique()
class_dict = {name: idx for idx, name in enumerate(class_names)}

# Labels klasörünün yolunu belirle
base_label_path = "data/labels"

# Eğer labels klasörü yoksa oluştur
if not os.path.exists(base_label_path):
    os.makedirs(base_label_path)

# Her bir set için klasör oluştur
for subset in ["train", "test", "val"]:
    subset_path = os.path.join(base_label_path, subset)
    if not os.path.exists(subset_path):
        os.makedirs(subset_path)

# Görüntü adına göre grupla ve her bir görüntü için bir .txt dosyası oluştur
for _, group in df.groupby("image_name"):
    # Dosya adını ve yolunu belirle
    subset = group["image_name"].values[0].split("_")[0]  # "train", "test" veya "val" al
    filename = group["image_name"].values[0].split(".")[0] + ".txt"  # "train_1" gibi
    filepath = os.path.join(base_label_path, subset, filename)
    
    # .txt dosyasına yaz
    with open(filepath, "w") as file:
        for index, row in group.iterrows():
            # Sınıf ID"si
            class_id = row["class"]
            # Normalleştirilmiş bounding box koordinatları
            x_center = (row["x1"] + row["x2"]) / 2 / row["width"]
            y_center = (row["y1"] + row["y2"]) / 2 / row["height"]
            width = (row["x2"] - row["x1"]) / row["width"]
            height = (row["y2"] - row["y1"]) / row["height"]

            class_id = class_dict[row["class"]]

            # Dosyaya yaz
            file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
