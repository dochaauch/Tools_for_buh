import pdfplumber
import re

def extract_and_process_text(pdf_path):
    output_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            regex = r'^(.*)\s(\d+)\s(\d+)$'

            for line in text.split("\n"):
                line = line.replace(',', '')
                match = re.match(regex, line)
                if match:
                    part1 = match.group(1).strip()
                    part2 = match.group(2).replace(" ", ",")
                    part3 = match.group(3).replace(" ", ",")
                    output_string = f"{part1},{part2},{part3}"
                    output_text += output_string + '\n'
                else:
                    output_text += line + '\n'
    return output_text

def write_to_txt_file(text, file_name):
    with open(file_name, 'w') as file:
        file.write(text)
        file.write('\n\n')

# Используем функции
pdf_path = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/doki/2022_Bilans_kasum.pdf'
text_output = extract_and_process_text(pdf_path)
write_to_txt_file(text_output, 'bilanss.txt')