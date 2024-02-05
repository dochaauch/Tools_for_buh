import fitz  # Импортируем PyMuPDF
from openpyxl import Workbook, load_workbook
import os
import re
from datetime import datetime


def read_highlighted_texts_and_comments(pdf_path):
    # print(f"Попытка открыть файл: {pdf_path}")  # Выводим имя файла перед открытием
    doc = fitz.open(pdf_path)
    highlighted_texts = []
    comments = []

    for page in doc:
        annotations = page.annots()
        if annotations:
            for annot in annotations:
                if annot.type[0] == 8:  # Highlight annotation
                    # Уменьшаем прямоугольник аннотации для уточнения области поиска
                    rect = annot.rect
                    adjusted_rect = fitz.Rect(rect.x0, rect.y0 + (rect.y1 - rect.y0) * 0.3, rect.x1, rect.y1 - (rect.y1 - rect.y0) * 0.3)
                    words = page.get_text("words")
                    highlighted_words = [w[4] for w in words if fitz.Rect(w[:4]).intersects(adjusted_rect)]
                    if highlighted_words:  # Если нашлись слова внутри аннотации
                        highlighted_text = " ".join(highlighted_words)
                        highlighted_texts.append(highlighted_text)
                        # Чтение комментария, если он есть
                        comment = annot.info['content'] if 'content' in annot.info else ''
                        comments.append(comment)

    doc.close()
    return highlighted_texts, comments


def calculate_km(sum_value, kokku_value):
    try:
        sum_float = parse_sum_to_float(sum_value) if sum_value else 0.0
        kokku_float = parse_sum_to_float(kokku_value) if kokku_value else sum_float
        return kokku_float - sum_float
    except ValueError:
        return 0.00  # или 0, если предпочтительнее возвращать 0 при ошибках преобразования


def process_highlighted_texts_and_comments(highlighted_texts, comments, predefined_keys):
    output_dict = {key: None for key in predefined_keys}
    unmatched_comments = []  # Для комментариев, не соответствующих ключам

    for text, comment in zip(highlighted_texts, comments):
        if comment in predefined_keys:
            if output_dict[comment] is None:
                output_dict[comment] = text
        else:
            unmatched_comments.append(comment)  # Собираем несоответствующие комментарии

    #print(output_dict)

    output_dict['km'] = calculate_km(output_dict.get('sum'), output_dict.get('kokku'))

    if output_dict["sum"] is not None:
        output_dict["sum"] = parse_sum_to_float(output_dict["sum"])
    if output_dict["kokku"] is not None:
        output_dict["kokku"] = parse_sum_to_float(output_dict["kokku"])

    if output_dict["date"] is not None:
        output_dict["date"] = format_date(output_dict["date"])
    if output_dict["date2"] is not None:
        output_dict["date2"] = format_date(output_dict["date2"])

    # Специальная обработка для некоторых ключей
    if output_dict["kokku"] is None:
        output_dict["kokku"] = output_dict["sum"]

    if output_dict["date2"] is None and output_dict["date"] is not None:
        output_dict["date2"] = output_dict["date"]
    if output_dict["cur"] is None:
        output_dict["cur"] = "EUR"

    if output_dict["our"] is None:
        output_dict["our"] = "_"

    #print(output_dict)

    return output_dict, unmatched_comments


def reverse_date_format(date_str):
    # Разделяем исходную строку даты на день, месяц и год
    day, month, year = date_str.split(".")
    # Извлекаем последние две цифры года и переставляем элементы в нужном порядке
    reversed_date = f"{year[-2:]}{month}{day}"
    return reversed_date


def parse_sum_to_float(value):
    # Извлекаем числа, пробелы (для тысяч) и запятую (как десятичный разделитель)
    numeric_value = re.sub(r"[^\d, ]", "", value)
    # Удаляем пробелы и заменяем запятую на точку для формата float
    normalized_value = numeric_value.replace(" ", "").replace(",", ".")
    return float(normalized_value)


def format_date(date_str):
    month_mapping = {
        "01": ["jaanuar", "january"],
        "02": ["veebruar", "february"],
        "03": ["märts", "march"],
        "04": ["aprill", "april"],
        "05": ["mai", "may"],
        "06": ["juuni", "june"],
        "07": ["juuli", "july"],
        "08": ["august", "august"],
        "09": ["september", "september"],
        "10": ["oktoober", "october"],
        "11": ["november", "november"],
        "12": ["detsember", "december"],
    }

    # Преобразование названия месяца в его числовой эквивалент
    date_str_processed = date_str.lower()
    for month_number, month_names in month_mapping.items():
        for month_name in month_names:
            if month_name in date_str_processed:
                replace_with = month_number + "."  # Добавляем точку после числа месяца
                date_str_processed = re.sub(month_name, replace_with, date_str_processed, flags=re.IGNORECASE)
                date_str_processed = date_str_processed.replace("..", ".")  # Удаляем двойные точки, если они есть
                break

    # Удаление лишних пробелов
    date_str_processed = re.sub(r'\s+', '', date_str_processed).strip()

    # Пытаемся разобрать обработанную строку даты
    formatted_date = parse_date_from_common_formats(date_str_processed)
    if formatted_date:
        return formatted_date

    # Если специфическая обработка не привела к успеху, пытаемся разобрать исходную строку
    return parse_date_from_common_formats(date_str)


def parse_date_from_common_formats(date_str):
    """
    Пытается разобрать дату из строки, используя список стандартных форматов.
    Возвращает форматированную строку даты "%d.%m.%Y" или None, если разбор не удался.
    """
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y", "%d-%m-%y", "%d/%m/%y", "%d.%m.%y"):
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime("%d.%m.%Y")
        except ValueError:
            continue
    return None



def write_to_excel(output_dict, excel_file_name, predefined_keys):
    # Проверка и инициализация рабочей книги Excel
    try:
        wb = load_workbook(excel_file_name)
    except FileNotFoundError:
        wb = Workbook()
    sheet = wb.active

    if sheet.max_row == 1 and all([cell.value is None for cell in sheet[1]]):
        # Если файл только что создан, добавляем заголовки столбцов
        for idx, key in enumerate(predefined_keys, 1):
            sheet.cell(row=1, column=idx, value=key)
        next_row = 2
    else:
        next_row = sheet.max_row + 1

    for idx, key in enumerate(predefined_keys, 1):
        value = output_dict.get(key, "")
        if isinstance(value, float):
            sheet.cell(row=next_row, column=idx, value=value)
        else:
            sheet.cell(row=next_row, column=idx, value=str(value))

    wb.save(excel_file_name)


def initialize_excel_file(excel_file_name, predefined_keys):
    wb = Workbook()
    sheet = wb.active
    # Добавляем названия столбцов в первую строку
    for idx, key in enumerate(predefined_keys, 1):
        sheet.cell(row=1, column=idx, value=key)
    wb.save(excel_file_name)


def rename_pdf_file(original_path, date_str, firma, invoice, is_kres_auto=False):
    date = datetime.strptime(date_str, "%d.%m.%Y")
    reverse_date = date.strftime("%y%m%d")

    # Определение формата нового имени файла в зависимости от условия
    if is_kres_auto:
        new_filename = f"Kres_{reverse_date}_{sanitize_filename(firma)}_arve.pdf"
    else:
        new_filename = f"{reverse_date}_{sanitize_filename(firma)}_{sanitize_filename(invoice)}.pdf"

    new_path = os.path.join(os.path.dirname(original_path), new_filename)

    try:
        os.rename(original_path, new_path)
        print(f"Файл '{original_path}' был переименован в '{new_filename}'")
    except OSError as error:
        print(f"Ошибка при переименовании файла: {error}")


def sanitize_filename(filename):
    """
    Удаляет недопустимые символы из имени файла и возвращает очищенное имя.
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    # Удаление конечных пробелов и точек из имени файла
    filename = filename.rstrip('. ')
    return filename


def process_all_pdfs_in_folder(folder_path, excel_file_name, predefined_keys):
    initialize_excel_file(excel_file_name, predefined_keys)

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            print(f"Обрабатываем файл: {file}")
            highlighted_texts, comments = read_highlighted_texts_and_comments(full_path)
            output_dict, unmatched_comments = process_highlighted_texts_and_comments(highlighted_texts, comments, predefined_keys)

            if unmatched_comments:
                print(f"Несоответствующие комментарии: {unmatched_comments}")

            none_keys = [key for key, value in output_dict.items() if value is None]
            if none_keys:
                print(f"Нет данных для ключей: {none_keys}")

            # Теперь правильно вызываем функцию записи в Excel
            write_to_excel(output_dict, excel_file_name, predefined_keys)

            # Интеграция функции переименования
            # Предположим, что `output_dict` содержит ключи 'date', 'firma', и 'invoice'
            date_str = output_dict.get('date')  # Например, '01.01.2024'
            firma = output_dict.get('firma')  # Например, 'YourCompany'
            arve = output_dict.get('arve')  # Например, '12345'

            if date_str and firma and arve:
                # Переименовываем файл
                is_kres_auto = "Kres" in output_dict.get("our", "")
                rename_pdf_file(full_path, date_str, firma, arve, is_kres_auto)
            else:
                print(f"Не удалось переименовать файл {file}, так как не все данные доступны.")



def main():
    folder_path = "/Users/docha/Library/CloudStorage/GoogleDrive-kres.auto79@gmail.com/Мой диск/2024-01"
    predefined_keys = ["firma", "date", "arve", "sum", "km", "kokku", "date2", "cur", "our"]

    # Формирование пути к файлу Excel внутри обрабатываемой папки
    excel_file_name = os.path.join(folder_path, "_all_invoices.xlsx")

    process_all_pdfs_in_folder(folder_path, excel_file_name, predefined_keys)


if __name__ == '__main__':
    main()
