import camelot

print(camelot.__version__)

# указываем путь к файлу PDF и используем метод `read_pdf` для чтения таблиц из PDF-файла
tables = camelot.read_pdf('/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/doki/2022_Bilans_kasum.pdf')

# выводим количество извлеченных таблиц
print('Количество таблиц: ', len(tables))

# перебираем таблицы и сохраняем их в формате CSV
for i, table in enumerate(tables):
    table.to_csv(f'output/table_{i+1}.csv')