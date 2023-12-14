import csv
from collections import Counter
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.multioutput import MultiOutputClassifier

# Функция для чтения данных из CSV файла
def read_csv(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        data = [row for row in reader]
    return data

# Преобразование данных для машинного обучения
def prepare_data_for_ml(data):
    X = []
    y_main = []
    y_add = []
    for row in data:
        main_numbers = eval(row[1])
        add_numbers = eval(row[2])
        # Создаем признаки для модели: количество каждого числа в основных и дополнительных номерах
        features = Counter(main_numbers + add_numbers)
        X.append([features.get(i, 0) for i in range(1, 51)])  # Для основных номеров от 1 до 50
        y_main.append(main_numbers)
        y_add.append(add_numbers)
    return X, y_main, y_add

# Обучение модели машинного обучения с использованием MultiOutputClassifier
def train_ml_model(X_train, y_train_main, y_train_add):
    model_main = RandomForestClassifier()
    model_add = RandomForestClassifier()
    multioutput_model_main = MultiOutputClassifier(model_main)
    multioutput_model_add = MultiOutputClassifier(model_add)
    multioutput_model_main.fit(X_train, y_train_main)
    multioutput_model_add.fit(X_train, y_train_add)
    return multioutput_model_main, multioutput_model_add

# Основной блок кода
if __name__ == '__main__':
    data = read_csv('eurojackpot_results.csv')
    X, y_main, y_add = prepare_data_for_ml(data)
    X_train, X_test, y_train_main, y_test_main, y_train_add, y_test_add = train_test_split(X, y_main, y_add,
                                                                                           test_size=0.2,
                                                                                           random_state=42)

    model_main, model_add = train_ml_model(X_train, y_train_main, y_train_add)

    # Предсказание и оценка модели
    predictions_main = model_main.predict(X_test)
    predictions_add = model_add.predict(X_test)

    # Оценка точности модели для основных номеров
    accuracy_main = accuracy_score(y_test_main, predictions_main, normalize=True)
    print(f'Точность модели для основных номеров: {accuracy_main}')

    # Оценка точности модели для дополнительных номеров
    accuracy_add = accuracy_score(y_test_add, predictions_add, normalize=True)
    print(f'Точность модели для дополнительных номеров: {accuracy_add}')
