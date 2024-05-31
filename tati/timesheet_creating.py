import pandas as pd
import os
from datetime import datetime, time, timedelta

import openpyxl


def read_excel_files_in_folder(folder_path):
    output_folder_path = os.path.join(folder_path, 'output')
    # Создаем папку output, если она еще не существует
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    all_data = []
    for file in files:
        print(f"Processing file: {file}")
        file_path = os.path.join(folder_path, file)
        data = read_data_from_worksheet(file_path)
        all_data.extend(data)

    # Агрегировать данные по месяцам
    aggregated_data_by_month = aggregate_data_by_month(all_data)

    # Создание и сохранение файлов по месяцам
    for month, data in aggregated_data_by_month.items():
        work_time_sheet = create_work_time_sheet(data, month)
        work_time_sheet = add_time_summary(work_time_sheet, data)  # Добавляем подсчет часов
        output_file_name = f"work_time_sheet_{month}.xlsx"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        work_time_sheet.to_excel(output_file_path, index=True)


def time_to_seconds(t):
    # Проверяем, является ли значение NaN
    if pd.isna(t):
        return 0  # Возвращаем 0 секунд для NaN значений

    # Если t является объектом datetime, извлекаем из него время
    if isinstance(t, datetime):
        t = t.time()

    if isinstance(t, time):
        return t.hour * 3600 + t.minute * 60 + t.second
    elif isinstance(t, float):  # Обработка float значений, если они представляют время в Excel
        # Преобразование float времени из Excel в секунды
        hours, remainder = divmod(t * 24, 1)
        minutes, seconds = divmod(remainder * 60, 1)
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds * 60)
    return 0  # Возвращает 0 секунд, если тип не поддерживается или значение NaN


def calculate_time_intervals(start, end):
    day_start = time_to_seconds(time(7, 0))
    evening_start = time_to_seconds(time(18, 0))
    night_start = time_to_seconds(time(23, 15))
    # Конец суток в секундах
    full_day = time_to_seconds(time(23, 59, 59)) + 1

    start_seconds = time_to_seconds(start)
    end_seconds = time_to_seconds(end)

    # Если конец рабочего дня на следующий день, добавляем полные сутки к конечному времени
    if start.date() != end.date():
        end_seconds += full_day

    day_hours = evening_hours = night_hours = 0

    # Рассчитываем пересечения с временными интервалами
    if start_seconds < evening_start:
        # Рабочее время начинается до конца дневного времени
        day_hours = max(0, min(end_seconds, evening_start) - start_seconds) / 3600
    if start_seconds < night_start and end_seconds > evening_start:
        # Рабочее время пересекает вечерний временной интервал
        evening_hours = max(0, min(end_seconds, night_start) - max(start_seconds, evening_start)) / 3600
    if end_seconds > night_start or start_seconds > night_start:
        # Рабочее время пересекает ночной временной интервал
        night_hours_start = max(start_seconds, night_start)
        night_hours_end = end_seconds if end_seconds > night_start else night_start
        if night_hours_end < night_hours_start:
            night_hours_end += full_day
        night_hours = (night_hours_end - night_hours_start) / 3600

    return day_hours, evening_hours, night_hours


def add_time_summary(df_final, aggregated_data):
    """Добавляет в DataFrame подсчет часов по времени суток."""
    # Добавляем заголовки для итоговых часов
    summary_headers = ['Päivä (07:00-18:00)', 'Ilta (18:00-23:15)', 'Yö (23:15-07:00)']
    for header in summary_headers:
        df_final[header] = 0

    for worker, dates_list in aggregated_data.items():
        #for dl in dates_list:
        #    print(dl)
        # Суммирование часов для каждого сотрудника
        day_total = sum(record['DayHours'] for record in dates_list)
        evening_total = sum(record['EveningHours'] for record in dates_list)
        night_total = sum(record['NightHours'] for record in dates_list)
        # print(worker, day_total, evening_total, night_total)

        # Округление до двух знаков после запятой
        df_final.loc[worker, 'Päivä (07:00-18:00)'] = round(day_total, 2)
        df_final.loc[worker, 'Ilta (18:00-23:15)'] = round(evening_total, 2)
        df_final.loc[worker, 'Yö (23:15-07:00)'] = round(night_total, 2)

    return df_final



def read_data_from_worksheet(file_path):
    df = pd.read_excel(file_path, sheet_name='Worksheet', engine='openpyxl')
    records = []
    for _, row in df.iterrows():
        if pd.isna(row['Alku']) or pd.isna(row['Loppu']) or pd.isna(row['Päivä']):
            continue

        start_time = row['Alku']
        end_time = row['Loppu']

        if end_time < start_time:
            end_time = datetime.combine((row['Päivä'] + pd.Timedelta(days=1)).date(), end_time)
        else:
            end_time = datetime.combine(row['Päivä'].date(), end_time)

        start_time = datetime.combine(row['Päivä'].date(), start_time)

        day_hours, evening_hours, night_hours = calculate_time_intervals(start_time, end_time)

        records.append({
            'Työntekijä': row['Työntekijä'],
            'Päivä': row['Päivä'].date(),
            'Alku': start_time,
            'Loppu': end_time,
            'DayHours': day_hours,
            'EveningHours': evening_hours,
            'NightHours': night_hours
        })
        #for record in records:
        #    print(record)
    return records



def aggregate_data_by_month(records):
    aggregated_data = {}
    for record in records:
        worker = record['Työntekijä']
        date = record['Päivä']
        month = date.strftime('%Y-%m')

        if month not in aggregated_data:
            aggregated_data[month] = {}
        if worker not in aggregated_data[month]:
            aggregated_data[month][worker] = []

        # Добавляем все записи в список для возможности их последующей агрегации
        aggregated_data[month][worker].append(record)
    return aggregated_data


def aggregate_intervals_by_date(records):
    intervals_by_date = {}
    for record in records:
        date_str = record['Päivä'].strftime('%Y-%m-%d')
        if date_str not in intervals_by_date:
            intervals_by_date[date_str] = []
        intervals_by_date[date_str].append((record['Alku'], record['Loppu']))
    return intervals_by_date


def create_work_time_sheet(aggregated_data, month):
    # Создаем DataFrame для итогового табеля
    year, month = map(int, month.split('-'))
    date_range = pd.date_range(start=datetime(year, month, 1),
                               end=datetime(year, month, 1).replace(day=28) + pd.offsets.MonthEnd(0))
    df_final = pd.DataFrame(columns=["Työntekijä"] + [date.strftime('%d.%m.%Y') for date in date_range])

    for worker, records in aggregated_data.items():
        intervals_by_date = aggregate_intervals_by_date(records)
        print(worker,intervals_by_date)
        worker_intervals = []
        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in intervals_by_date:
                # Получаем первое время начала и последнее время окончания для этой даты без сортировки
                start_time = intervals_by_date[date_str][0][0].strftime('%H:%M')  # Первый интервал начала
                end_time = intervals_by_date[date_str][-1][1].strftime('%H:%M')
                worker_intervals.append(f"{start_time} - {end_time}")
            else:
                worker_intervals.append('')  # Нет работы в этот день
        df_final = df_final.append(
            {"Työntekijä": worker, **dict(zip([date.strftime('%d.%m.%Y') for date in date_range], worker_intervals))},
            ignore_index=True)

    df_final.set_index("Työntekijä", inplace=True)
    return df_final



def main():
    #folder_path = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/Maalaus/Ermail'
    folder_path = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/Maalaus/240522'
    read_excel_files_in_folder(folder_path)

if __name__ == '__main__':
    main()
