import os

def list_files(directory, extensions):
    files_list = []  # Создаем пустой список для хранения названий файлов
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                files_list.append(file)  # Добавляем название файла в список
    files_list.sort()  # Сортируем список файлов
    for file in files_list:
        print(file)  # Выводим отсортированные названия файлов

# Замените 'your_directory_path' на путь к вашей папке.
if __name__ == "__main__":
    directory_path = '/Users/docha/Library/CloudStorage/GoogleDrive-kres.auto79@gmail.com/Мой диск/2023-12'
    extensions = ('.jpg', '.pdf')
    list_files(directory_path, extensions)


