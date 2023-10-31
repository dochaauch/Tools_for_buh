import os
import shutil

def check_conflicts(src_folder, dest_folder):
    dest_cheki_folder = os.path.join(dest_folder, '_cheki')
    if os.path.exists(dest_cheki_folder):
        src_files = os.listdir(src_folder)
        conflicting_files = []

        for file_name in src_files:
            dest_file_path = os.path.join(dest_cheki_folder, file_name)
            if os.path.exists(dest_file_path):
                conflicting_files.append(file_name)

        return conflicting_files
    else:
        return []


def handle_conflicts(src_folder, dest_folder, conflicting_files):
    dest_cheki_folder = os.path.join(dest_folder, '_cheki')
    for file_name in conflicting_files:
        src_file_path = os.path.join(src_folder, file_name)
        dest_file_path = os.path.join(dest_cheki_folder, file_name)

        # Check if the file already exists in the destination folder
        if os.path.exists(dest_file_path):
            index = 1
            while True:
                # Generate a new filename by adding the index as a prefix
                new_file_name = f"{index}_{file_name}"
                new_dest_file_path = os.path.join(dest_cheki_folder, new_file_name)
                if not os.path.exists(new_dest_file_path):
                    dest_file_path = new_dest_file_path
                    break
                index += 1

        print(f'Конфликт: файл {file_name} уже существует в папке {dest_cheki_folder}.')
        print(f'Переименованный файл: {os.path.basename(dest_file_path)}')




def merge_folders(src_folder, dest_folder):
    conflicting_files = check_conflicts(src_folder, dest_folder)
    if conflicting_files:
        handle_conflicts(src_folder, dest_folder, conflicting_files)
    #else:
    dest_cheki_folder = os.path.join(dest_folder, '_cheki')
    shutil.copytree(src_folder, dest_cheki_folder)


def main():
    #src_folder = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Metsa10/_cheki'
    src_folder = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Metsa10/_cheki'
    #dest_folder = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Metsa10/2023'
    dest_folder = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Metsa10/2023'
    merge_folders(src_folder, dest_folder)


if __name__ == '__main__':
    main()
