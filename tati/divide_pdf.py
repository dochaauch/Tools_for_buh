import PyPDF2
import openpyxl
import os

# Открываем PDF-файл и Excel-файл
pdf_file_path = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/Maalaus/order.pdf'
excel_file_path = '/Users/docha/Library/CloudStorage/OneDrive-Личная/Leka/Maalaus/ListOfNames.xlsx'

# Получаем путь к директории, где находится PDF-файл
output_directory = os.path.dirname(pdf_file_path)

pdf_reader = PyPDF2.PdfFileReader(pdf_file_path)
excel_workbook = openpyxl.load_workbook(excel_file_path)
excel_sheet = excel_workbook.active

# Проходим по каждой строке в Excel-файле и создаем новый PDF-файл для каждой строки
for index, row in enumerate(excel_sheet.iter_rows(min_row=2, values_only=True), start=1):
    full_name = row[1]  # Фамилия и имя во втором столбце (B)
    if full_name:
        print(full_name)
        last_name, first_name = full_name.split()  # Разделяем фамилию и имя

        # Создаем новый PDF-файл с одной страницей
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(index - 1))  # Используем индекс для выбора соответствующей страницы

        # Сохраняем новый PDF-файл с соответствующим именем
        output_pdf_file_name = os.path.join(output_directory, f'{last_name}_{first_name}_contract_appendix_2023-10.pdf')
        with open(output_pdf_file_name, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)

# Закрываем Excel-файл
excel_workbook.close()
