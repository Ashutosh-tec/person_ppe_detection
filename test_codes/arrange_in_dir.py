import os
import shutil
import random
import re

def replace_str(text:str, old_folder:str="images", new_folder:str="")->str:
    # Define the regex pattern to match '/images/'
    pattern = rf'/{old_folder}'
    # Replace all occurrences of the pattern with '/labels/'
    replaced_text = re.sub(pattern, f'/{new_folder}', text)
    return replaced_text

def change_extension(filename:str, new_extension:str)->str:
    """
    Change the previous extension to new.
    """
    # Split the filename into the base and the extension
    base = os.path.splitext(filename)[0]
    # Create the new filename with the new extension
    new_filename = f"{base}.{new_extension}"
    return new_filename

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def split_data(source_dir, destination_dir, train_pct, test_pct, image_folder:str="images", label_folder:str="labels"):
    
    # for destination of image
    train_dir = os.path.join(destination_dir, "train")   
    test_dir = os.path.join(destination_dir, "test")   
    val_dir = os.path.join(destination_dir, "val")   
    # Create target directories
    create_directory(train_dir)
    create_directory(test_dir)
    create_directory(val_dir)
    
    # for destination of labels
    train_dir_label = os.path.join(replace_str(destination_dir, new_folder="labels"), "train")   
    test_dir_label = os.path.join(replace_str(destination_dir, new_folder="labels"), "test")   
    val_dir_label = os.path.join(replace_str(destination_dir, new_folder="labels"), "val") 
    print("@@@@@@@ train_dir_label: ", train_dir_label)  
    # Create target directories
    create_directory(train_dir_label)
    create_directory(test_dir_label)
    create_directory(val_dir_label)


    # Get list of all files in the source directory
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    random.shuffle(files)  # Shuffle the files randomly

    total_files = len(files)
    train_count = int(total_files * train_pct / 100)
    test_count = int(total_files * test_pct / 100)
    val_count = total_files - train_count - test_count  # Remaining files go to validation

    train_files = files[:train_count]
    test_files = files[train_count:train_count + test_count]
    val_files = files[train_count + test_count:]

    # copy files to corresponding directories
    for file in train_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(train_dir, file))
        print("####################################")
        print(source_dir, file)
        print(train_dir)
        print(os.path.join(replace_str(train_dir, "labels")))#, change_extension(file, "txt")))

        print("$$$$ Folder: ", os.path.join(replace_str(source_dir, new_folder=label_folder), change_extension(file, "txt")))
        print("####################################")
        shutil.copy(os.path.join(replace_str(source_dir, old_folder=image_folder, new_folder=label_folder), change_extension(file, "txt")), 
                    os.path.join(replace_str(train_dir_label, new_folder="labels"), change_extension(file, "txt")))
    for file in test_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(test_dir, file))
        shutil.copy(os.path.join(replace_str(source_dir, old_folder=image_folder, new_folder=label_folder), change_extension(file, "txt")), 
                    os.path.join(replace_str(test_dir_label, new_folder="labels"), change_extension(file, "txt")))

    for file in val_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(val_dir, file))
        shutil.copy(os.path.join(replace_str(source_dir, old_folder=image_folder, new_folder=label_folder), change_extension(file, "txt")), 
                    os.path.join(replace_str(val_dir_label, new_folder="labels"), change_extension(file, "txt")))

    print(f'Total files: {total_files}')
    print(f'Train files: {len(train_files)}')
    print(f'Test files: {len(test_files)}')
    print(f'Validation files: {len(val_files)}')

# Define paths
source_dir = '/mnt/d/Codes/ppe_yolov8/datasets/images_ppe'
destination_dir = '/mnt/d/Codes/ppe_yolov8/ppe_dataset/images'

# Define percentages
train_pct = 70
test_pct = 10
val_pct = 20

# Split the data
split_data(source_dir, destination_dir, train_pct, test_pct, image_folder = "images_ppe", label_folder = "labels_yolo_ppe")
