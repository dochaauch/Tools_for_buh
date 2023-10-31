import shutil
import pandas as pd
import glob
import os


def combine_all_csv(folder_path):
    # Чтение всех файлов CSV, начинающихся с 'combine' в указанной папке
    csv_files = glob.glob(folder_path + '/combine*.csv')
    # Создание пустого DataFrame для объединения данных
    combined_data = pd.DataFrame()
    # Чтение и объединение файлов CSV
    for file in csv_files:
        # Чтение данных из файла CSV
        data = pd.read_csv(file)
        # Добавление данных в объединенный DataFrame
        combined_data = pd.concat([combined_data, data], ignore_index=True)

    # Преобразование 'kuupaev' в формат даты
    combined_data['kuupaev'] = pd.to_datetime(combined_data['kuupaev'], format='%d.%m.%y', errors='coerce')

    # Сортировка данных по столбцу 'kuupaev'
    combined_data = combined_data.sort_values(by='kuupaev')

    # Преобразование 'kuupaev' обратно в исходный формат
    combined_data['kuupaev'] = combined_data['kuupaev'].dt.strftime('%d.%m.%y')

    # Восстановление столбца индекса
    #combined_data = combined_data.reset_index(drop=True)

    # Добавление столбца со сквозными индексами в начало DataFrame
    #combined_data.insert(0, 'index', combined_data.index)

    # Удаление первого столбца (индекса)
    combined_data = combined_data.iloc[:, 1:]

    # Сохранение объединенных данных в новом файле CSV в той же папке, что и folder_path
    save_path = folder_path + '/combine_total.csv'
    combined_data.to_csv(save_path, index=False)

    move_files_to_done(csv_files, folder_path)


def move_files_to_done(csv_files, folder_path):
    # Создание папки "done", если она не существует
    done_folder = folder_path + '/done'
    os.makedirs(done_folder, exist_ok=True)

    # Перемещение обработанных файлов в папку "done"
    for file in csv_files:
        file_name = os.path.basename(file)  # Извлекаем только имя файла
        if file_name != 'combine_total.csv':
            destination = os.path.join(done_folder, file_name)  # Полный путь к файлу назначения
            shutil.move(file, destination)


def main():
    # Путь к папке с файлами CSV
    folder_path = '/Users/docha/Desktop/test'
    combine_all_csv(folder_path)


if __name__ == '__main__':
    main()
