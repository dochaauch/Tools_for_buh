import pdfplumber
import re

# Открываем PDF-файл
with pdfplumber.open('/Users/docha/Google Диск/Bonus/doki/2022_Bilans_kasum.pdf') as pdf:
    output_text = ""

    # Проходим по всем страницам PDF-файла
    for page in pdf.pages:

        # Извлекаем текст из текущей страницы
        text = page.extract_text()

        #regex = r'^(\d+\.\s*[A-Z\s]+)(\d*\s*\d*)\s+(\d*\s*\d*)'
        regex = r'^(.*)\s(\d+)\s(\d+)$'

        for line in text.split("\n"):
            line = line.replace(',', '')
            #print(line)
            match = re.match(regex, line)
            if match:
                part1 = match.group(1).strip()
                part2 = match.group(2).replace(" ", ",")
                part3 = match.group(3).replace(" ", ",")
                output_string = f"{part1},{part2},{part3}"
                output_text += output_string + '\n'
                print(output_string)
            else:
                output_text += line + '\n'
                #print("***", line)


        # Открываем текстовый файл для записи в режиме добавления
        with open('bilanss.txt', 'w') as file:

            # Записываем текст из текущей страницы в текстовый файл
            file.write(output_text)

            # Добавляем разделитель между страницами
            file.write('\n\n')