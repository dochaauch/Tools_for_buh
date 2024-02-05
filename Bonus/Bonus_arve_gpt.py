import datetime
import os
import re
import codecs
import PyPDF2
import pdfplumber

from tika import parser

os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'

def str_to_float(s):
    return float(s.replace(',', '.'))


def collect_list_of_files(target_folder):
    #your_target_folder = "/Users/docha/Google Диск/Bonus/2023-01/"
    pdf_files = []
    for dirpath, _, filenames in os.walk(target_folder):
        for items in filenames:
            file_full_path = os.path.abspath(os.path.join(dirpath, items))
            #if file_full_path.lower().endswith(".pdf"): #ищем все pdf файлы в папке
            r1 = re.compile('\/\d{6}.*\.pdf$')  #  вводим паттерн, который будем искать (название только 6 цифр)
            if r1.search(file_full_path.lower()):  #  ищем наш паттерн в полном пути файла
                pdf_files.append(file_full_path)
            else:
                pass
    return pdf_files


def merge_pdfs(pdf_files):
    pdf_files.sort(key=str.lower)
    pdf_writer = PyPDF2.PdfFileWriter()

    for file_path in pdf_files:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page_num))

    with open('merged.pdf', 'wb') as pdf_output:
        pdf_writer.write(pdf_output)


# def read_pdf_content(file_path):
#     raw = parser.from_file(file_path)
#     raw = raw['content']
#
#     special_char_map = {ord('ä'): 'a', ord('ü'): 'u', ord('ö'): 'o', ord('õ'): 'o',
#                         ord('ž'): 'z', ord('š'): 's',
#                         ord('Ä'): 'A', ord('Ü'): 'U', ord('Ö'): 'O', ord('Õ'): 'O',
#                         ord('Z'): 'Z', ord('Š'): 's', ord('’'): ''}
#     raw = raw.translate(special_char_map)
#     raw = re.sub(r'\n+\s*\n*', '\n', raw.strip())
#     raw = raw.replace('\\n', '\n')
#     return raw

def read_pdf_content(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text



def write_output(lists, file_path):
    with open(file_path, 'w') as f:
        first_row = ('D' + '\t' + 'kuupaev'.ljust(10) + '\t' + 'maksepaev' + '\t' + 'klient'.ljust(20)
                     + '\t' + 'arve'.center(8) + '\t' + 'kokku'.center(9) + '\t' + 'kaibemaks'.center(7)
                     + '\t' + 'KMta'.ljust(7) + '\n')
        f.write(first_row)
        print(first_row)

        # Инициализация переменных до цикла
        client = ""
        invoice = ""
        amount = 0.00
        percentage = 0.00
        total = 0.00
        payment_date = ""

        for l in lists:
            if "KLIENT:" in l:
                client = l.replace("KLIENT:", "").strip()
            if "ARVE:" in l:
                invoice = l.replace("ARVE:", "").strip()
            if "Summa KM-ta:" in l:
                amount = str_to_float(l.replace("Summa KM-ta:", "").strip())
            if "Kibemaks 20%:" in l:
                percentage = str_to_float(l.replace("Kibemaks 20%:", "").strip())
            if "Kokku:" in l:
                total = str_to_float(l.replace("Kokku:", "").strip())
            if "Maksethtaeg:" in l:
                payment_date = l.replace("Maksethtaeg:", "").strip()

            # Проверка наличия всех данных перед формированием строки
            if payment_date and client and invoice:
                row = ('D' + '\t' + payment_date.ljust(10) + '\t' + client.ljust(20)
                       + '\t' + invoice.ljust(20) + '\t' + "{:.2f}".format(amount).rjust(10)
                       + '\t' + "{:.2f}".format(percentage).rjust(10) + '\t'
                       + "{:.2f}".format(total).rjust(10) + '\n')
                f.write(row)
                payment_date = ""
                client = ""
                invoice = ""

        print("Data written to " + file_path)


def main():
    target_folder = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/2023-11"
    pdf_files = collect_list_of_files(target_folder)
    merge_pdfs(pdf_files)
    write_output(read_pdf_content('merged.pdf'), 'output.txt')

if __name__ == '__main__':
        main()