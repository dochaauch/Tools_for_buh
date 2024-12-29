import pandas as pd
from datetime import datetime, timedelta

def calculate_schengen_days(data, date):
    result = []
    date = datetime.strptime(date, "%Y-%m-%d")
    lookback_date = date - timedelta(days=180)

    for _, row in data.iterrows():
        person_name = f"{row['Perekonnanimi']} {row['Eesnimed']}"
        start_dates = pd.to_datetime(row['Alguskuupäev'].split(','), format="%d.%m.%Y")

        end_dates = pd.to_datetime(row['Lõppkuupäev'].split(','), format="%d.%m.%Y")

        # Уникальные дни пребывания
        all_unique_days = set()

        for start, end in zip(start_dates, end_dates):
            if end >= lookback_date and start <= date:
                overlap_start = max(start, lookback_date)
                overlap_end = min(end, date)

                # Добавляем дни пересечения в итоговый набор
                current_days = set(overlap_start + timedelta(days=i) for i in range((overlap_end - overlap_start).days + 1))
                all_unique_days.update(current_days)

        # Вывод итогового набора уникальных дней для отладки
        #print(f"{person_name}: num: {len(sorted([d.strftime('%Y-%m-%d') for d in all_unique_days]))} Уникальные дни (итог): {sorted([d.strftime('%Y-%m-%d') for d in all_unique_days])}")

        total_days = len(all_unique_days)

        # Построчный расчет с деталями
        result.append({
            "Perekonnanimi": row['Perekonnanimi'],
            "Eesnimed": row['Eesnimed'],
            "nr": row['номер справки'],
            "lookback_date": lookback_date.strftime("%d.%m.%Y"),
            "alguskuupäev": start_dates[0],
            "lõppkuupäev": end_dates[0],
            "Unique Schengen Days": total_days,
            #"Used Days": sorted(list(all_unique_days)),
            "Calculation Date": date.strftime("%d.%m.%Y"),
            "meie": row['meie'],
            "status": row['status']
        })

    result_df = pd.DataFrame(result)


    result_df = result_df.sort_values(by=["Perekonnanimi", "Eesnimed", "alguskuupäev"])
    result_df['alguskuupäev'] = pd.to_datetime(result_df['alguskuupäev']).dt.strftime("%d.%m.%Y")
    result_df['lõppkuupäev'] = pd.to_datetime(result_df['lõppkuupäev']).dt.strftime("%d.%m.%Y")

    return result_df

def generate_grouped_report(result_df):
    grouped_result = result_df.groupby(["Perekonnanimi", "Eesnimed", "Calculation Date", ], as_index=False).sum()
    return grouped_result


def main():
    try:
        # Загрузка данных
        data_active = pd.read_excel(file_path, engine="openpyxl")
        data_inactive = pd.read_excel(file_path_inact, engine="openpyxl")

        # Проверка необходимых столбцов
        required_columns = ["Perekonnanimi", "Eesnimed", "Alguskuupäev", "Lõppkuupäev"]
        for df in [data_active, data_inactive]:
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файлы должны содержать столбцы: Perekonnanimi, Eesnimed, Alguskuupäev, Lõppkuupäev")

        # Объединение датафреймов
        combined_data = pd.concat([data_active, data_inactive], ignore_index=True)

        # Удаление дубликатов, если требуется
        combined_data = combined_data.drop_duplicates()

        # Расчет дней Шенгена
        result_df = calculate_schengen_days(combined_data, calc_date)
        print("Результат расчета (построчно):")
        print(result_df.to_string())

        grouped_df = generate_grouped_report(result_df)
        print("Сгруппированный результат:")
        print(grouped_df.to_string())

        # Сохранение результатов в Excel
        output_path = file_path.replace('_combine.xlsx', '_result.xlsx')
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            result_df.to_excel(writer, sheet_name="Построчные расчеты", index=False)
            grouped_df.to_excel(writer, sheet_name="Сгруппированные расчеты", index=False)

        print(f"Результаты сохранены в файл: {output_path}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    #file_path = input("Введите путь к файлу (xlsx): ")
    file_path = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/A1 calculation/_combine.xlsx'
    file_path_inact = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/A1 calculation/_inact_process.xlsx'
    #calc_date = input("Введите дату для расчета (ГГГГ-ММ-ДД): ")
    calc_date = '2024-12-28'

    main()
