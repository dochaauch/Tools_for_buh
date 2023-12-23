import pprint

import openpyxl


def read_excel(file_name, sheet_name):
    workbook = openpyxl.load_workbook(file_name, data_only=True)
    sheet = workbook[sheet_name]

    # Чтение заголовков из первой и второй строки
    headers_row_1 = [cell.value for cell in sheet[1]]
    headers_row_2 = [cell.value for cell in sheet[2]]

    # Объединение заголовков из первой и второй строки
    headers = [f'{r1}//{r2}' if r1 else r2 for r1, r2 in zip(headers_row_1, headers_row_2)]

    # Чтение данных, начиная с третьей строки
    svod_data = []
    for row in sheet.iter_rows(min_row=3, values_only=True):
        row_data = {headers[i]: cell for i, cell in enumerate(row)}
        svod_data.append(row_data)

    return svod_data


def create_new_sheet_with_headers(file_name, new_sheet_name, headers):
    workbook = openpyxl.load_workbook(file_name)

    # Проверка наличия листа и его удаление при необходимости
    if new_sheet_name in workbook.sheetnames:
        del workbook[new_sheet_name]

    # Создание нового листа и добавление заголовков
    new_sheet = workbook.create_sheet(new_sheet_name)
    new_sheet.append(headers)

    # Сохранение изменений в файле
    workbook.save(file_name)


def extract_expence_accs_by_prefix(row, prefix):
    accounts = []
    for key, value in row.items():
        if key.startswith(prefix) and value is not None:
            parts = key.split('//')
            account_number = parts[0]
            account_description = parts[1] if len(parts) > 1 else ''  # Описание счета, если оно есть
            accounts.append((account_number, account_description, value))
    return accounts

def process_sheet_data_for_new_sheet(svod_data, column_mappings, headers, kaibemaks, kaibemaksuta_desc):
    zagruzka_data = []
    document_start_index = 0

    for row in svod_data:
        expense_accounts = extract_expence_accs_by_prefix(row, expence_account_prefix)  # Извлекает счета расходов
        km_o_total_for_row = 0
        total_sum_for_doc = 0

        if not expense_accounts:
            expense_accounts = [('', None)]

        for account, account_desc, sum_value in expense_accounts:
            new_row, km_o_value, summa_total = create_row_for_zagruzka(row, account, account_desc,
                                                          sum_value, kaibemaks, kaibemaksuta_desc, headers)
            km_o_total_for_row += km_o_value
            total_sum_for_doc += summa_total

            for header, svod_key in column_mappings.items():
                new_row[header] = row.get(svod_key, '')

            zagruzka_data.append(new_row)

        if km_o_total_for_row != round(row.get('km', 0), 2):
            correct_km_o_values(zagruzka_data, document_start_index, km_o_total_for_row, row)

        #Пересчитываем общую сумму после корректировки НСО
        recalculated_total_sum = sum(float(r['Сумма с НСО']) for r in zagruzka_data[document_start_index:])

        if round(recalculated_total_sum,2) != round(row.get('summa kokku', 0), 2):
            correct_total_sum(zagruzka_data, document_start_index, recalculated_total_sum, row)

        document_start_index = len(zagruzka_data)

    return zagruzka_data


def create_row_for_zagruzka(row, account, account_desc, sum_value, kaibemaks, kaibemaksuta_desc, headers):
    new_row = {header: '' for header in headers}
    new_row['Счет'] = account
    new_row['Сумма'] = str(sum_value) if sum_value is not None else ''

    if account_desc not in kaibemaksuta_desc and sum_value is not None:
        km_o_value = round(sum_value * kaibemaks, 2)
        new_row['Ставка НСО'] = f'{int(kaibemaks * 100)}%'
        new_row['Комментарий'] = row.get('kirjeldus', '')
    else:
        km_o_value = 0
        new_row['Ставка НСО'] = 'Нет'
        new_row['Комментарий'] = account_desc

    summa_total = sum_value + km_o_value

    new_row['Сумма НСО'] = f'{km_o_value:.2f}'
    new_row['Сумма с НСО'] = f'{summa_total:.2f}'
    return new_row, km_o_value, summa_total


def correct_km_o_values(zagruzka_data, document_start_index, km_o_total_for_row, row):
    document_id = row.get('arve nr', '')
    km_value = round(row.get('km', 0), 2)

    for correction_row in reversed(zagruzka_data[document_start_index:]):
        existing_km_o_value = float(correction_row['Сумма НСО']) if correction_row['Сумма НСО'] else 0
        if existing_km_o_value != 0:
            correction = km_value - km_o_total_for_row
            corrected_km_o_value = existing_km_o_value + correction
            correction_row['Сумма НСО'] = f"{corrected_km_o_value:.2f}"
            correction_row['Сумма с НСО'] = f"{float(correction_row['Сумма с НСО']) + correction:.2f}"
            print(f"Документ {document_id}, {row.get('firma', )}: Старый налог {existing_km_o_value:.2f},"
                  f" новый налог {corrected_km_o_value:.2f}, "
                  f"сумма с НСО старая {float(correction_row['Сумма с НСО']):.2f},"
                  f" сумма с НСО новая {float(correction_row['Сумма с НСО']) + correction:.2f}")
            break


def correct_total_sum(zagruzka_data, document_start_index, total_sum_for_document, row):
    document_id = row.get('arve nr', '')
    summa_kokku = round(row.get('summa kokku', 0), 2)

    for correction_row in reversed(zagruzka_data[document_start_index:]):
        existing_sum = float(correction_row['Сумма с НСО']) if correction_row['Сумма с НСО'] else 0
        if existing_sum != 0 and correction_row['Ставка НСО'] != 'Нет':
            correction = summa_kokku - total_sum_for_document
            corrected_sum = existing_sum + correction
            correction_row['Сумма с НСО'] = f"{corrected_sum:.2f}"
            print(f"Документ {document_id}, {row.get('firma', )}: "
                  f"Старая сумма {existing_sum:.2f}, новая сумма {corrected_sum:.2f}, "
                  f"коррекция {correction:.2f}")
            break



def write_data_to_sheet(file_name, sheet_name, data, headers):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook[sheet_name]

    for row_data in data:
        row_values = [row_data.get(header, '') for header in headers]  # Преобразование словаря в список
        sheet.append(row_values)

    workbook.save(file_name)



if __name__ == '__main__':
    file_path = "/Users/docha/PycharmProjects/Tools_for_buh/Kres/test/_svod_2312.xlsx"
    sheet_name = "svod"
    new_sheet_name = "zagruzka"
    kaibemaks = 0.2
    expence_account_prefix = '4'

    headers = [
        'Вид бухгалтерской операции',
        'Счет',
        'Контрагент НСО',
        'Дата документа',
        'Вид документа НСО',
        'Серия документа',
        'Номер документа',
        'Валюта отчета',
        'Курс валюты отчета',
        'Сумма',
        'Ставка НСО',
        'Сумма НСО',
        'Сумма с НСО',
        'Счет проводки НСО',
        'Применение НСО',
        'Аналитика по НСО',
        'Счет 50%',
        'Субконто1',
        'Субконто2',
        'Субконто3',
        'Субконто4',
        'Субконто5',
        'Субконто1 50%',
        'Субконто2 50%',
        'Субконто3 50%',
        'Субконто4 50%',
        'Субконто5 50%',
        'Основание',
        'Комментарий',
    ]  # Все 29 заголовков столбцов на новом листе (1c)

    kaibemaksuta_desc = [
        'pant',
    ]

    column_mappings = {
        'Контрагент НСО': 'reg nr',
        'Дата документа': 'kuupaev',
        'Номер документа': 'arve nr',
    } # Соответствия заголовков столбцов 1С и их имен в исходном файле

    data = read_excel(file_path, sheet_name)
    #pprint.pprint(data)

    create_new_sheet_with_headers(file_path, new_sheet_name, headers)

    processed_data = process_sheet_data_for_new_sheet(data, column_mappings,headers, kaibemaks, kaibemaksuta_desc)
    #pprint.pprint(processed_data)
    write_data_to_sheet(file_path, new_sheet_name, processed_data, headers)
