import pandas as pd

def read_and_rename_columns(file_path, sheet_name=None, column_mapping=None):
    """
    Читает Excel файл, создаёт DataFrame и переименовывает столбцы.

    :param file_path: str, путь к файлу Excel
    :param sheet_name: str, название листа (если None, читается первый лист)
    :param column_mapping: dict, словарь для переименования столбцов (например, {"OldName": "NewName"})
    :return: pd.DataFrame
    """
    # Чтение Excel файла
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

    # Если задано переименование столбцов
    if column_mapping:
        df.rename(columns=column_mapping, inplace=True)

    return df

def add_name_columns(df, source_column, last_name_column, first_name_column):
    """
    Добавляет столбцы с фамилией и именем, разделяя значения из исходного столбца.

    :param df: pd.DataFrame, датафрейм
    :param source_column: str, название исходного столбца
    :param last_name_column: str, название столбца для фамилии
    :param first_name_column: str, название столбца для имени
    :return: pd.DataFrame
    """
    # Разделяем значения на имя и фамилию, затем меняем местами
    def split_name(value):
        parts = value.split(" ", 1)
        if len(parts) == 2:
            return parts[1], parts[0]  # Возвращаем фамилию, затем имя
        return "", value  # Если нет пробела, предполагаем, что это только имя

    df[[last_name_column, first_name_column]] = df[source_column].apply(lambda x: pd.Series(split_name(str(x))))
    return df

def split_period_column(df, source_column, start_date_column, end_date_column):
    """
    Делит столбец периода на два столбца: начало и конец периода.

    :param df: pd.DataFrame, датафрейм
    :param source_column: str, название исходного столбца с периодом
    :param start_date_column: str, название столбца для начальной даты
    :param end_date_column: str, название столбца для конечной даты
    :return: pd.DataFrame
    """
    # Разделяем значения на начальную и конечную дату
    df[[start_date_column, end_date_column]] = df[source_column].str.split(" - ", expand=True)
    return df

def reorder_and_remove_columns(df, column_order, columns_to_remove):
    """
    Изменяет порядок столбцов и удаляет указанные столбцы.

    :param df: pd.DataFrame, датафрейм
    :param column_order: list, порядок столбцов
    :param columns_to_remove: list, список столбцов для удаления
    :return: pd.DataFrame
    """
    # Удаляем ненужные столбцы
    df = df.drop(columns=columns_to_remove, errors="ignore")

    # Изменяем порядок столбцов
    df = df[column_order]

    return df

def main(file_path):
    sheet_name = "Лист1"  # Явно указываем лист
    column_mapping = {
        "Tõendi number": "номер справки",
        "Tööandja": "meie",
        "Tõend/taotlus tühistati": "Lõppkuupäev",
    }  # Словарь для переименования

    dataframe = read_and_rename_columns(file_path, sheet_name, column_mapping)

    # Добавляем столбцы фамилии и имени
    dataframe = add_name_columns(dataframe, source_column="Töötaja", last_name_column="Perekonnanimi",
                                 first_name_column="Eesnimed")

    # Разделяем столбец периода на начало и конец
    dataframe = split_period_column(dataframe, source_column="Periood", start_date_column="Alguskuupäev",
                                    end_date_column="Lõppkuupäev_original")

    # Преобразуем столбец "Lõppkuupäev" в формат DD.MM.YYYY
    dataframe["Lõppkuupäev"] = pd.to_datetime(dataframe["Lõppkuupäev"],
                                                        errors="coerce").dt.strftime("%d.%m.%Y")

    # Добавляем столбец status с значением "INACT"
    dataframe["status"] = "INACT"

    # Определяем новый порядок столбцов и столбцы для удаления
    new_column_order = ["номер справки", "Perekonnanimi", "Eesnimed", "Alguskuupäev", "Lõppkuupäev",
                        "Lõppkuupäev_original", "meie", "status"]
    columns_to_remove = ["Töötaja", "Periood"]

    # Изменяем порядок столбцов и удаляем ненужные
    dataframe = reorder_and_remove_columns(dataframe, column_order=new_column_order,
                                           columns_to_remove=columns_to_remove)

    # Исключаем строки, где "номер справки" == NaN
    dataframe = dataframe.dropna(subset=["номер справки"])

    # Исключаем строки, где "Alguskuupäev" равен "Lõppkuupäev"
    dataframe = dataframe[dataframe["Alguskuupäev"] != dataframe["Lõppkuupäev"]]

    # Сохраняем DataFrame в новый Excel файл
    output_file_path = file_path.replace("inactive A1.xlsx", "_inact_process.xlsx")
    dataframe.to_excel(output_file_path, index=False, engine="openpyxl")

    # Вывод первых строк DataFrame
    print(dataframe.to_string())



if __name__ == "__main__":
    # Пример использования
    file_path = "/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/A1 calculation/inactive A1.xlsx"  # Путь к файлу
    result = main(file_path)

