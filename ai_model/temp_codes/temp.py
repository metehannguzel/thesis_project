import pandas as pd
import os
from tqdm import tqdm

# CSV dosyasını yükle
df = pd.read_csv("annotations/annotations_train_new_classes.csv")

# Her bir klasör için dosyaları kontrol et
folders = ["train", "test", "val"]
for folder in folders:
    # Belirli bir klasördeki tüm dosya isimlerini al
    files = os.listdir(f"data/images/{folder}")
    
    # Her bir dosya için
    for image in tqdm(files, desc=f"{folder} için..."):
        # Dosya adını kullanarak CSV"deki ilgili satırları bul ve güncelle
        number = image.split("_")[1]  # numarayı dosya adından al
        df.loc[df["image_name"] == f"train_{number}", "image_name"] = f"{folder}_{number}"

df.tail()

df.to_csv("annotations/annotations_train_test_val_new_classes.csv", index=False)


####################################################################################################

import os

# Dosya isimlerini değiştireceğiniz ana dizin yolu
base_directory = "data/labels"

# "test" ve "val" klasörleri için işlem yapılacak
folders = ["test"]

# Her klasör için işlem yap
for folder in folders:
    # Klasör yolu
    folder_path = os.path.join(base_directory, folder)
    
    # Klasördeki tüm dosyaları listele
    for filename in os.listdir(folder_path):
        if filename.startswith("test_"):
            # Yeni dosya adını oluştur (örn. "train_" yerine "test_" veya "val_")
            new_name = filename.replace("test_", "train_")
            # Dosya yolu
            old_file = os.path.join(folder_path, filename)
            # Yeni dosya yolu
            new_file = os.path.join(folder_path, new_name)
            # Dosyayı yeniden adlandır
            os.rename(old_file, new_file)

print("Dosya isimleri başarıyla değiştirildi.")


####################################################################################################

import pandas as pd

df = pd.read_csv("annotations/annotations_train_test_val_new_classes.csv")

filtered_df = df[df["image_name"].str.startswith("val_")]

unique_count = filtered_df["image_name"].nunique()
