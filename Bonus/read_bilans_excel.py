import pdfplumber
import pandas as pd
import re
from openpyxl.utils import get_column_letter


def process_pdf_page(page):
    data = []
    text = page.extract_text()
    regex = r'(.*)\s{1,2}(-?\d+)?\s{2}(-?\d+)?\s+$'

    for line in text.split("\n"):
        line = line.replace(',', '')
        match = re.match(regex, line)
        if match:
            # Извлекаем данные в отдельные столбцы
            part1 = match.group(1).strip()
            part2 = match.group(2)
            part3 = match.group(3)
            data.append([part1, part2, part3])
        else:
            # Если строка не соответствует шаблону, добавляем её целиком в первый столбец
            data.append([line, '', ''])
    return data


def adjust_column_width(sheet):
    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[get_column_letter(column_cells[0].column)].width = length


def write_to_excel(pdf_path, excel_file_name):
    with pdfplumber.open(pdf_path) as pdf:
        with pd.ExcelWriter(excel_file_name, engine='openpyxl') as writer:
            for i, page in enumerate(pdf.pages):
                data = process_pdf_page(page)
                df = pd.DataFrame(data, columns=['Column1', 'Column2', 'Column3'])
                df['Column2'] = pd.to_numeric(df['Column2'], errors='coerce')
                df['Column3'] = pd.to_numeric(df['Column3'], errors='coerce')
                df.to_excel(writer, sheet_name=f'Page {i+1}', index=False)

                # Получаем доступ к последнему добавленному листу
                workbook = writer.book
                sheet_names = list(writer.sheets)  # Преобразуем dict_keys в список
                sheet = workbook[sheet_names[-1]]
                adjust_column_width(sheet)




def main():
    pdf_path = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/doki/2022_Bilans_kasum.pdf'
    excel_file_name = 'bilanss.xlsx'
    write_to_excel(pdf_path, excel_file_name)



# Используем функции
if __name__ == '__main__':
    main()
    print('Готово!')

