import datetime
import pprint
from PIL import Image
import os
import datetime


def search_all_png_files(your_target_folder):
    file_dict = {}
    for file_names in os.walk(your_target_folder):
        root, dirs, file_list = file_names
        for file_ in file_list:
            if file_.endswith('.png'):
                file_date_ = os.stat(os.path.join(root, file_)).st_birthtime
                file_date = datetime.datetime.fromtimestamp(file_date_).strftime('%y%m%d_%H%M')
                file_dict[os.path.join(root, file_)] = file_date
    #pprint.pprint(file_dict)
    return file_dict


def main():
    your_target_folder = '/Users/docha/Google Диск/Metsa10'
    file_dict = search_all_png_files(your_target_folder)
    for old_path, file_date in file_dict.items():
        old_name = os.path.basename(old_path).split('.')[0]
        new_name = f'{file_date}_{old_name}.jpg'
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        print(old_path, new_path)
        im1 = Image.open(old_path)
        im1.save(new_path)


if __name__ == '__main__':
    main()

