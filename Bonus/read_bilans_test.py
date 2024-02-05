import pdfplumber
import pandas as pd

def convert_pdf_to_excel(pdf_path, excel_path):
    with pdfplumber.open(pdf_path) as pdf:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    # Создаем DataFrame с одной колонкой
                    df = pd.DataFrame(text.split('\n'), columns=['Content'])
                    # Записываем DataFrame в Excel на отдельном листе
                    sheet_name = f'Page {i+1}'
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

# Путь к PDF и Excel файлам
pdf_path = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/doki/2022_Bilans_kasum.pdf'
excel_path = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/doki/file.xlsx'

# Вызов функции конвертации
convert_pdf_to_excel(pdf_path, excel_path)
