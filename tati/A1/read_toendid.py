import os
import pandas as pd
import pdfplumber
from colorama import Fore, Style, init
import numpy as np
from read_inact_xlsx import main as read_inact_xlsx

init(autoreset=True)

def get_pdf_files_from_folder(folder_path):
    """
    Получает список всех PDF-файлов в указанной папке.

    :param folder_path: Путь к папке
    :return: Список путей к PDF-файлам
    """
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.pdf')]

def extract_relevant_data_from_text(text):
    """
    Извлекает релевантные данные из текста PDF.

    :param text: Содержимое текста PDF
    :return: Словарь с ключевыми данными
    """
    data = {}
    lines = text.splitlines()
    #print(lines)

    # Извлечение номера справки (первая строка)
    data['номер справки'] = lines[0].strip() if lines else ""

    # Извлечение имени, фамилии, и других данных
    for i, line in enumerate(lines):
        if "Perekonnanimi" in line:
            data['Perekonnanimi'] = line.split(" ")[3].strip()
        elif "Eesnimed" in line:
            data['Eesnimed'] = line.split(" ")[3].strip()
        elif "Isikukood" in line:
            data['Isikukood'] = line.split(" ")[3].strip()
        elif "Nimi või ärinimi" in line:
            parts = line.strip().split(" ")
            data['meie'] = ' '.join(parts[6:])
        elif "Alguskuupäev" in line and "Lõppkuupäev" in line:
            parts = line.split(" ")
            data['Alguskuupäev'] = parts[3].strip()
            data['Lõppkuupäev'] = parts[7].strip()
        elif "Teid palkava(te) äriühingu(te)" in line and i + 1 < len(lines):
            parts = lines[i + 1].strip().split(" ")
            data['firma'] = ' '.join(parts[0:-1])
        elif "Laeva(de) aadress(id) või nimi" in line and i + 2 < len(lines):
            parts = lines[i + 2].strip().split(" ")
            data['Koht'] = ' '.join(parts[-3:]).replace(".", " ")

    return data

def rename_file(original_path, data):
    """
    Переименовывает файл в формате Perekonnanimi_Eesnimed_YYMMDD_YYMMDD.pdf

    :param original_path: Исходный путь к файлу
    :param data: Словарь с извлечёнными данными
    :return: Новый путь к файлу
    """
    folder, original_name = os.path.split(original_path)

    # Проверяем, что данные корректны
    if (all(value in ["", "Unknown", np.nan] for value in data.values()) or
            not data.get('номер справки', '').startswith('SKA')):
        print(Fore.YELLOW + f"Файл оставлен без изменений: {original_name}")
        return original_path  # Возвращаем исходный путь, если данные некорректны или номер справки не начинается с 'SKA'

    # Форматирование дат
    algus_date = data.get('Alguskuupäev', '')
    lopp_date = data.get('Lõppkuupäev', '')

    def format_date(date_str):
        try:
            day, month, year = date_str.split('.')
            return f"{year[-2:]}{month}{day}"
        except ValueError:
            return "Unknown"

    algus_formatted = format_date(algus_date)
    lopp_formatted = format_date(lopp_date)
    meie = data.get('meie', '')

    # Создание нового имени
    new_name = f"{data.get('Perekonnanimi', 'Unknown')}_{data.get('Eesnimed', 'Unknown')}_{algus_formatted}_{lopp_formatted}_{meie}.pdf"
    new_path = os.path.join(folder, new_name)

    # Переименование файла
    os.rename(original_path, new_path)
    return new_path

def extract_text_and_tables_from_pdf(pdf_path):
    """
    Извлекает текст и таблицы из PDF-файла.

    :param pdf_path: Путь к PDF-файлу
    :return: Словарь с текстом и таблицами
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return extract_relevant_data_from_text(text)
    except Exception as e:
        print(Fore.RED + f"Ошибка при обработке файла {pdf_path}: {e}")
        return {}

def create_dataframe_from_pdfs(folder_path, status):
    """
    Создает DataFrame из данных всех PDF-файлов в указанной папке.

    :param folder_path: Путь к папке
    :param status: Статус документов (ACTV или CNCL)
    :return: DataFrame с релевантными данными
    """
    pdf_files = get_pdf_files_from_folder(folder_path)
    data = []

    for pdf_file in pdf_files:
        print(Fore.CYAN + f"Обработка файла: {os.path.basename(pdf_file)}")
        extracted_data = extract_text_and_tables_from_pdf(pdf_file)
        new_path = rename_file(pdf_file, extracted_data)
        extracted_data['filename'] = os.path.basename(new_path)
        extracted_data['status'] = status
        data.append(extracted_data)

    return pd.DataFrame(data)

def save_dataframe_to_excel(df, folder_path):
    """
    Сохраняет DataFrame в Excel-файл.

    :param df: DataFrame
    :param output_path: Путь к Excel-файлу
    """
    output_path = os.path.join(folder_path, "_combine.xlsx")
    df.to_excel(output_path, index=False)

def main():
    """
    Основная функция. Задает папку и выводит результат.
    """
    folder_path = "/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/A1 calculation"  # Замените на путь к папке с PDF-файлами
    status_input = input(Fore.LIGHTCYAN_EX + "Введите статус документов (оставьте пустым для Active, введите 'Canceled' для Canceled): ").strip()
    status = "CNCL" if status_input.lower() == "canceled" else "ACTV"

    df = create_dataframe_from_pdfs(folder_path, status)
    print(Fore.LIGHTMAGENTA_EX + f'{df.to_string()}')  # Выводим DataFrame в консоль в виде строки
    save_dataframe_to_excel(df, folder_path)

    #read_inact_xlsx.main("/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/A1 calculation/inactive A1.xlsx")

if __name__ == "__main__":
    main()
