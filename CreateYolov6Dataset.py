import os
import shutil
from pathlib import Path
import Util


class DataSetManger:

    def __init__(self):
        self.image_source_folder = \
            "/home/dev-team/Documents/Yolov6DataSets/RoboFlow1/images/valid"
        self.label_source_folder = \
            "/home/dev-team/Documents/Yolov6DataSets/RoboFlow1/labels/valid"

        self.image_destination_folder = "./DataSet/images/"
        self.label_destination_folder = "./DataSet/labels/"

        # train test valid
        self.train_data, self.test_data, self.valid_data = (0.8, 0.15, 0.05)

    # iterating over all the files in labels folder
    def get_total_files_count(self):
        file_count = 0
        for filename in os.listdir(self.label_source_folder):
            label_file_source_path = os.path.join(self.label_source_folder, filename)
            file_size = os.path.getsize(label_file_source_path)

            if file_size > 0:
                file_count += 1
        return file_count

    def copy_label_and_images(self):
        if not Util.is_folder_exist(self.image_destination_folder, self.label_destination_folder):
            Util.create_dataset_folder()
        utilObj = Util.DataSetUtil(self.image_source_folder, self.label_source_folder)
        if utilObj.is_data_valid():
            total_file_count = self.get_total_files_count()
            training_data_count, test_data_count, validation_data_count = self.split_dataset(total_file_count)
            print(f"Total files = {total_file_count} \n"
                  f"Training files = {training_data_count} \n"
                  f"Testing files = {test_data_count} \n"
                  f"Validation files = {validation_data_count}")

            for filename in os.listdir(self.label_source_folder):
                label_file_source_path = os.path.join(self.label_source_folder, filename)
                file_size = os.path.getsize(label_file_source_path)

                if file_size > 0:
                    image_file_source_path = os.path.join(self.image_source_folder, filename.replace(".txt", ".jpg"))
                    path = Path(image_file_source_path)
                    if path.is_file():
                        if training_data_count > 0:
                            sub_folder = "train"
                            self.set_destination_and_copy_files(filename, label_file_source_path,
                                                                image_file_source_path, sub_folder)
                            training_data_count -= 1
                        else:
                            if test_data_count > 0:
                                sub_folder = "test"
                                self.set_destination_and_copy_files(filename, label_file_source_path,
                                                                    image_file_source_path, sub_folder)
                                test_data_count -= 1

                            else:
                                if validation_data_count > 0:
                                    sub_folder = "valid"
                                    self.set_destination_and_copy_files(filename, label_file_source_path,
                                                                        image_file_source_path, sub_folder)
                                    validation_data_count -= 1
                    else:
                        print(f"{image_file_source_path} doesn't exist.")
        else:
            print(f"Invalid data {self.image_source_folder}")

    def set_destination_and_copy_files(self, filename, label_file_source_path, image_file_source_path, sub_folder):
        label_file_destination_path = os.path.join(self.label_destination_folder, sub_folder, filename)
        image_file_destination_path = os.path.join(self.image_destination_folder, sub_folder,
                                                   filename.replace(".txt", ".jpg"))

        shutil.copy(label_file_source_path, label_file_destination_path)
        shutil.copy(image_file_source_path, image_file_destination_path)

    def split_dataset(self, total_files):
        training_data_count = round(self.train_data * total_files)
        testing_data_count = round(self.test_data * total_files)
        validation_data_count = round(self.valid_data * total_files)

        return training_data_count, testing_data_count, validation_data_count


if __name__ == '__main__':
    dataSetManager = DataSetManger()
    dataSetManager.copy_label_and_images()
