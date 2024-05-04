import os
import pandas as pd

output_folder = "labels"

annotations = pd.read_csv("annotations_train_2.csv")
class_names = annotations["class"].unique()
class_dict = {name: idx for idx, name in enumerate(class_names)}

for image_name, group in annotations.groupby("image_name"):
    txt_file_path = os.path.join(output_folder, image_name.replace(".jpg", ".txt"))
    with open(txt_file_path, "w") as f:
        for _, row in group.iterrows():
            x_center = ((row["x1"] + row["x2"]) / 2) / row["width"]
            y_center = ((row["y1"] + row["y2"]) / 2) / row["height"]
            bbox_width = (row["x2"] - row["x1"]) / row["width"]
            bbox_height = (row["y2"] - row["y1"]) / row["height"]
            
            class_id = class_dict[row["class"]]
            
            f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# {'water_and_drinks': 0, 'healthcare': 1, 'personal_care': 2, 'home': 3, 'food': 4, 'pets': 5}