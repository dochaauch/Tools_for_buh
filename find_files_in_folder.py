import os
import pprint


def search_all_special_files(your_target_folder, file_dict, exten):
    for file_names in os.walk(your_target_folder):
        root, dirs, file_list = file_names
        for file_ in file_list:
            if file_.endswith(exten):
                # размер файлов в мегабайтах
                size_of_file = round(float(os.path.getsize(os.path.join(root, file_)) / (1024 * 1024)), 2)
                file_dict[os.path.join(root, file_)] = size_of_file


def main():
    your_target_folder = '/Users/docha/Google Диск/Bonus'
    file_dict = {}
    search_all_special_files(your_target_folder, file_dict, '.zip')
    pprint.pprint(file_dict)
    dictTotal = sum(value for value in file_dict.values())
    print('всего размер удаляемых файлов', dictTotal)  # всего размер всех файлов в мегабайтах

    #  удаляем файлы
    #for file_ in file_dict.keys():
        #os.remove(file_)


if __name__ == '__main__':
    main()
