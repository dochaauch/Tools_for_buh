from conv_jpg_crop import crop_image
import os
import datetime

def search_all_png_files(your_target_folder):
    file_dict = {}
    for file_names in os.walk(your_target_folder):
        root, dirs, file_list = file_names
        for file_ in file_list:
            if file_.endswith('.jpg'):
                file_date_ = os.stat(os.path.join(root, file_)).st_birthtime
                file_date = datetime.datetime.fromtimestamp(file_date_).strftime('%y%m%d_%H%M')
                file_dict[os.path.join(root, file_)] = file_date
    #pprint.pprint(file_dict)
    return file_dict

def main():
    your_target_folder = '/Users/docha/Desktop/Tsekkid 0502'
    file_dict = search_all_png_files(your_target_folder)
    for file_path in file_dict.keys():
        print(file_path)
        crop_image(file_path)


if __name__ == '__main__':
    main()