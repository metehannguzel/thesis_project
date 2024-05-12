import os
import shutil
from random import shuffle

def split_data(source_folder, train_folder, test_folder, val_folder, train_size=0.8, test_size=0.1):
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    shuffle(files)

    train_count = int(len(files) * train_size)
    test_count = int(len(files) * test_size)
    val_count = len(files) - train_count - test_count

    for folder in [train_folder, test_folder, val_folder]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    for i, file in enumerate(files):
        if i < train_count:
            shutil.move(os.path.join(source_folder, file), os.path.join(train_folder, file))
        elif i < train_count + test_count:
            shutil.move(os.path.join(source_folder, file), os.path.join(test_folder, file))
        else:
            shutil.move(os.path.join(source_folder, file), os.path.join(val_folder, file))

source_folder = "data/images"
train_folder = "data/images/train"
test_folder = "data/images/test"
val_folder = "data/images/val"

split_data(source_folder, train_folder, test_folder, val_folder)



####################################################################################################

