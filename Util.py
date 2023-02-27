import os
from pathlib import Path


def is_folder_exist(*folder_paths):
    for folder_path in folder_paths:
        path = Path(folder_path)
        if not path.is_dir():
            return False
    return True


def create_dataset_folder():
    dataset_directories_list = ["DataSet1/images/test", "DataSet1/images/train", "DataSet1/images/valid",
                                "DataSet1/labels/test", "DataSet1/labels/train", "DataSet1/labels/valid"]
    for path in dataset_directories_list:
        if not os.path.exists(path):
            os.makedirs(path)


# size greater than 0 bytes
def get_valid_files_count(folder_path):
    valid_file_count = 0
    for filename in os.listdir(folder_path):
        file_source_path = os.path.join(folder_path, filename)
        file_size = os.path.getsize(file_source_path)
        if file_size > 0:
            valid_file_count += 1
    return valid_file_count


def get_total_files_count(folder_path):
    file_count = 0
    for _ in os.listdir(folder_path):
        file_count += 1
    return file_count


class DataSetUtil:
    def __init__(self, image_folder_path, label_folder_path):
        self.image_source_folder = image_folder_path
        self.label_source_folder = label_folder_path

    def is_data_valid(self):
        if not self.is_image_missing() and not self.is_image_missing():
            return True
        else:
            return False

    def is_label_missing(self):
        missing_count = 0
        for filename in os.listdir(self.image_source_folder):
            label_file_source_path = os.path.join(self.label_source_folder, filename.replace(".jpg", ".txt", ))
            path = Path(label_file_source_path)
            if not path.is_file():
                missing_count += 1
        if missing_count == 0:
            return False
        else:
            return True

    def is_image_missing(self):
        missing_count = 0
        for filename in os.listdir(self.label_source_folder):
            image_file_source_path = os.path.join(self.image_source_folder, filename.replace(".txt", ".jpg"))
            path = Path(image_file_source_path)
            if not path.is_file():
                print(image_file_source_path)
                missing_count += 1
        if missing_count == 0:
            return False
        else:
            return True
