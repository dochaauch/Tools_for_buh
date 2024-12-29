from datetime import datetime

# Функция для обработки строки с парами дат
def process_date_pairs(input_string):
    # Разделение строки на строки дат
    lines = input_string.strip().split("\n")
    for line in lines:
        # Разделение каждой строки на две даты
        start_date, end_date = line.split("\t")
        # Преобразование строк в объекты datetime
        start = datetime.strptime(start_date, "%d.%m.%Y")
        end = datetime.strptime(end_date, "%d.%m.%Y")
        # Вычисление разницы в днях
        delta = (end - start).days
        # Вывод результата
        print(f"Пара дат: {start_date} - {end_date}, Количество дней: {delta}")

# Пример строки
input_string = """
10.11.2024	27.12.2024
25.05.2024	30.06.2024
25.05.2024	23.12.2024
30.06.2024	23.12.2024
"""

# Обработка строки
process_date_pairs(input_string)
