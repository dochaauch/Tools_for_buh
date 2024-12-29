import pandas as pd
import os


def convert_csv_to_xlsx(file_path):
    # Чтение CSV-файла
    df = pd.read_csv(file_path)

    # Формирование пути для сохранения файла
    base_name = os.path.splitext(file_path)[0]
    new_file_path = f"{base_name}.xlsx"

    # Сохранение в формате Excel
    df.to_excel(new_file_path, index=False)
    print(f"Файл сохранен как: {new_file_path}")


# Укажите путь к вашему CSV-файлу
csv_file_path = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/2024-11/bolt/Bolt - Klientide kviitungid - Detsember 2024.csv"
convert_csv_to_xlsx(csv_file_path)
