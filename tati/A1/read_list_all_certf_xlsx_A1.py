import pandas as pd
from datetime import timedelta
from openpyxl import load_workbook
from openpyxl.styles import numbers


def read_excel_file(file_path):
    """Чтение файла Excel и создание DataFrame."""
    df = pd.read_excel(file_path, engine="openpyxl")
    # Удаляем столбцы, начинающиеся с "Unnamed:"
    unnamed_cols = [col for col in df.columns if str(col).startswith('Unnamed:')]
    df = df.drop(columns=unnamed_cols)
    return df


def process_data(df):
    """Обработка данных: разделение столбцов и преобразование дат."""
    # Разделение столбца Töötaja на имя и фамилию
    df[['Eesnimi', 'Perekonnanimi']] = df['Töötaja'].str.split(' ', n=1, expand=True)

    # Разделение столбца Periood на две части
    df[['alg', 'lopp']] = df['Periood'].str.split(' - ', expand=True)

    # Преобразование столбцов alg и lopp в формат datetime
    df['alg'] = pd.to_datetime(df['alg'], format='%d.%m.%Y', errors='coerce')
    df['lopp'] = pd.to_datetime(df['lopp'], format='%d.%m.%Y', errors='coerce')

    # Если в столбце Tõend/taotlus tühistati есть дата, используем её как lopp
    df['lopp'] = pd.to_datetime(df['Tõend/taotlus tühistati'], errors='coerce').combine_first(df['lopp'])

    # Сортировка по фамилии, имени и дате начала
    df = df.sort_values(['Perekonnanimi', 'Eesnimi', 'alg'])

    return df


def calculate_schengen_days_per_row(df, calculation_date):
    """Расчет количества шенгенских дней для каждой строки за последние 180 дней."""
    calculation_date = pd.to_datetime(calculation_date, format='%d.%m.%Y')
    start_date = calculation_date - timedelta(days=180)

    df['start_date'] = start_date
    df['calculation_date'] = calculation_date

    def calculate_days(row):
        # Если статус "Tagasi lükatud", возвращаем 0 дней
        if row['Olek'] == 'Tagasi lükatud':
            return 0
        # Иначе выполняем обычный расчет
        return max(min(row['lopp'], calculation_date) - max(row['alg'], start_date), timedelta(0)).days

    df['schengen_days'] = df.apply(calculate_days, axis=1)
    return df


def save_to_excel(df, file_path):
    """Сохранение DataFrame в Excel с форматированием дат."""
    # Сохраняем данные в Excel
    with pd.ExcelWriter(file_path, engine='openpyxl', datetime_format='dd.mm.yyyy') as writer:
        # Первый лист: исходные данные
        df.to_excel(writer, sheet_name='Исходные данные', index=False)

        # Применяем форматирование к конкретным столбцам
        workbook = writer.book
        worksheet = writer.sheets['Исходные данные']

        # Получаем индексы столбцов с датами
        date_columns = ['alg', 'lopp', 'start_date', 'calculation_date']
        for col_name in date_columns:
            if col_name in df.columns:
                col_letter = chr(65 + df.columns.get_loc(col_name))  # Получаем букву столбца
                for cell in worksheet[col_letter]:
                    if cell.row > 1:  # Пропускаем заголовок
                        cell.number_format = 'dd.mm.yyyy'

        # Второй лист: сгруппированные данные
        grouped_df = df.groupby(['Perekonnanimi', 'Eesnimi', 'calculation_date'], as_index=False).agg({
            'schengen_days': 'sum'
        })
        # Сортировка сгруппированных данных
        grouped_df = grouped_df.sort_values(['Perekonnanimi', 'Eesnimi'])
        grouped_df.to_excel(writer, sheet_name='Сгруппированные данные', index=False)

        # Форматируем даты на втором листе
        worksheet2 = writer.sheets['Сгруппированные данные']
        date_col = chr(65 + list(grouped_df.columns).index('calculation_date'))
        for cell in worksheet2[date_col]:
            if cell.row > 1:
                cell.number_format = 'dd.mm.yyyy'


def main(file_path, calculation_date):
    df = read_excel_file(file_path)
    df = process_data(df)
    df = calculate_schengen_days_per_row(df, calculation_date)

    result_file_path = file_path.replace('LIST OF ALL CERTS.xlsx', '_list_cert_result.xlsx')
    save_to_excel(df, result_file_path)
    print(f"Обработка завершена. Результат сохранен в '{result_file_path}'.")


if __name__ == "__main__":
    file_path = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/A1 calculation/LIST OF ALL CERTS.xlsx'
    calculation_date = '31.12.2024'
    main(file_path, calculation_date)