import pandas as pd
import os
import openpyxl

# Папка с исходными файлами
source_folder = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/Maalaus/Ermail'
# Папка для сохранения итогового файла
output_folder = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/Maalaus/Ermail/output/'
win_path = 'W:\\Leka\\Maalaus\\Ermail\\'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Инициализация пустого списка для сбора данных из всех файлов
all_data = []

# Проходимся по всем файлам в папке
for file in os.listdir(source_folder):
    if file.endswith('.xlsx'):
        # Считываем данные, пропуская заголовки, так как мы добавим их позже
        df = pd.read_excel(os.path.join(source_folder, file), skiprows=0, engine='openpyxl')

        # Добавляем столбец с именем файла
        df['FileName'] = file

        # Добавляем столбец с кликабельной ссылкой на файл
        # Обратите внимание на формат формулы HYPERLINK
        df['FileLink'] = '=HYPERLINK("' + win_path + file + '", "Open")'

        # Добавляем DataFrame в список
        all_data.append(df)

# Объединяем все DataFrame в один
combined_df = pd.concat(all_data, ignore_index=True)

# Удаляем возможные дубликаты заголовков, если они есть
combined_df = combined_df.loc[combined_df.index.drop_duplicates()]

# Сохраняем итоговый DataFrame в файл
combined_file_path = os.path.join(output_folder, 'combined_file.xlsx')
combined_df.to_excel(combined_file_path, index=False)

print(f'Combined file saved to {combined_file_path}')
