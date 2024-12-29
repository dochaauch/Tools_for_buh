import datetime
import os
import re
import pdfplumber

def str_to_float(str_value):
    return float(str_value.replace(',', '.'))

your_target_folder = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/\u041c\u043e\u0439 \u0434\u0438\u0441\u043a/Bonus/2024-11"

# Поиск всех файлов PDF в указанной папке с использованием регулярного выражения для имени файла
pdf_files = [
    os.path.abspath(os.path.join(dirpath, items))
    for dirpath, _, filenames in os.walk(your_target_folder)
    for items in filenames
    if re.search(r'/\d{6}.*\.pdf$', os.path.abspath(os.path.join(dirpath, items)).lower())
]

pdf_files.sort(key=str.lower)

# Объединение PDF-файлов с использованием pdfplumber
raw_text = ""
for files_address in pdf_files:
    with pdfplumber.open(files_address) as pdf:
        raw_text += "\n".join(page.extract_text() for page in pdf.pages if page.extract_text()) + "\n"

# Очистка и обработка текста
special_char_map = str.maketrans('äüöõžšÄÜÖÕŠ’', 'auoozsAUOOs ')
raw_text = raw_text.translate(special_char_map)
raw_text = re.sub(r'\n+\s*\n*', '\n', raw_text.strip())

lines = raw_text.splitlines()

# Запись результатов в файл output.txt
with open('output.txt', 'w') as f:
    first_row = ('D' + '\t' + 'kuupaev'.ljust(10) + '\t' + 'maksepaev' + '\t' + 'klient'.ljust(20)
                 + '\t' + 'arve'.center(8) + '\t' + 'kokku'.center(9) + '\t' + 'kaibemaks'.center(7) + '\t' + 'KMta'.ljust(7) + '\n')
    f.write(first_row)
    print(first_row)

    Skta = Skm = Skokk = 0.00
    current_data = {}

    for line in lines:
        if 'KLIENT' in line:
            current_data['klient'] = line.split(':')[1].split(',')[0].strip().ljust(25)
        elif 'ARVE' in line:
            current_data['arve'] = re.search(r'(\d+)', line).group(1)
        elif 'Summa KM-ta:' in line:
            current_data['summaKMta'] = re.search(r'(\d+,\d+)', line).group(1).rjust(9)
            Skta += str_to_float(current_data['summaKMta'])
        elif any(k in line for k in ['Kaibemaks 20%:', 'Käibemaks 20%:', 'Käibemaks 22%:', 'Kaibemaks 22%:']):
            current_data['kibemaks'] = re.search(r'(\d+,\d+)', line).group(1).rjust(7)
            Skm += str_to_float(current_data['kibemaks'])
        elif 'Kokku:' in line:
            current_data['kokku'] = re.search(r'(\d+,\d+)', line).group(1).rjust(9)
            Skokk += str_to_float(current_data['kokku'])
        elif 'Kuupaev:' in line:
            current_data['kuupaev'] = line.strip().replace(' ', '')[8:18]
            current_data['maksepaev'] = line.strip().replace(' ', '')[-13:-3]

            d1 = datetime.datetime.strptime(current_data['kuupaev'], '%d.%m.%Y')
            try:
                d2 = datetime.datetime.strptime(current_data['maksepaev'], '%d.%m.%Y')
                diffDate = str((d2 - d1).days)
            except ValueError:
                diffDate = ''

            if all(key in current_data for key in ['klient', 'arve', 'summaKMta', 'kibemaks', 'kokku', 'kuupaev', 'maksepaev']):
                tt = f"{diffDate}\t{current_data['kuupaev']}\t{current_data['maksepaev']}\t{current_data['klient']}\t{current_data['arve']}\t{current_data['kokku']}\t{current_data['kibemaks']}\t{current_data['summaKMta']}"
                print(tt)
                f.write(tt + '\n')
                current_data.clear()

    # Итоговая строка
    t_it = ('\n' + ''.rjust(3) + '\t' + ''.rjust(10) + '\t' + ''.rjust(10) + '\t' + ''.rjust(20) + '\t' + ''.rjust(6) + '\t'
            + '\t' + str(format(Skokk, '.2f')).rjust(9) + '\t' + str(format(Skm, '.2f')).rjust(7)
            + '\t' + str(format(Skta, '.2f')).rjust(9))
    print(t_it)
    f.write(t_it + '\n')
