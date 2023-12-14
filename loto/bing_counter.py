import csv
from collections import Counter

# Функция для чтения данных из CSV файла
def read_csv(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        main_numbers = []
        add_numbers = []
        for row in reader:
            main_numbers.extend(eval(row[1]))
            add_numbers.extend(eval(row[2]))
        return main_numbers, add_numbers

# Функция для нахождения наиболее вероятных номеров
def find_most_probable_numbers(main_numbers, add_numbers):
    main_number_counts = Counter(main_numbers)
    add_number_counts = Counter(add_numbers)
    most_common_main = [num for num, count in main_number_counts.most_common(5)]
    most_common_add = [num for num, count in add_number_counts.most_common(2)]
    return most_common_main, most_common_add

# Основной блок кода
if __name__ == '__main__':
    main_numbers, add_numbers = read_csv('eurojackpot_results.csv')
    most_probable_main, most_probable_add = find_most_probable_numbers(main_numbers, add_numbers)
    print(f'Наиболее вероятные основные номера: {most_probable_main}')
    print(f'Наиболее вероятные дополнительные номера: {most_probable_add}')