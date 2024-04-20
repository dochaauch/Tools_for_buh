import zipfile
import os

#your_target_folder = "/Users/docha/Google Диск/Bonus/2023-06/"
your_target_folder = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/2024-03/"

for file_ in os.listdir(your_target_folder):
    if file_.endswith('.zip'):
        path_to_zip_file = os.path.join(your_target_folder, file_)
        with zipfile.ZipFile(path_to_zip_file) as zip_ref:
            zip_ref.extractall(your_target_folder)
