#чтение счетов Bonus из всей папки в таблицу
#from tika import parser

import datetime


import os
import pprint
import re
import codecs
import PyPDF2
import pdfplumber

#os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'

import tika
from tika import parser

import re


def str_to_float(str):
    return float(str.replace(',', '.'))


your_target_folder = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/2023-09"

pdf_files = []

for dirpath, _, filenames in os.walk(your_target_folder):

    for items in filenames:

        file_full_path = os.path.abspath(os.path.join(dirpath, items))


        #if file_full_path.lower().endswith(".pdf"): #ищем все pdf файлы в папке
        r1 = re.compile('\/\d{6}.*\.pdf$')  #  вводим паттерн, который будем искать (название только 6 цифр)
        if r1.search(file_full_path.lower()):  #  ищем наш паттерн в полном пути файла
            pdf_files.append(file_full_path)


        else:
            pass


pdf_files.sort(key=str.lower)
pdfWriter = PyPDF2.PdfFileWriter()

for files_address in pdf_files:
    pdfFileObj = open(files_address, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    for pageNum in range(0, len(pdfReader.pages)):
        pageObj = pdfReader.pages[pageNum]


        #pdfWriter.add_page(pageObj)
        pdfWriter.addPage(pageObj)



pdfOutput = open('merged.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()


raw = parser.from_file("merged.pdf")
raw = raw['content']

special_char_map = {ord('ä'): 'a', ord('ü'): 'u', ord('ö'): 'o', ord('õ'): 'o',
                   ord('ž'): 'z', ord('š'): 's',
                   ord('Ä'): 'A', ord('Ü'): 'U', ord('Ö'): 'O', ord('Õ'): 'O',
                   ord('Z'): 'Z', ord('Š'): 's', ord('’'): '',
                   }

# raw = ''
# with pdfplumber.open("merged.pdf") as pdf:
#     for pdf_reader in pdf.pages:
#         raw += pdf_reader.extract_text()
raw = raw.translate(special_char_map)

raw = re.sub('\n+\s*\n*', '\n', raw.strip())

raw = raw.replace('\\n', '\n')



safe_text = raw.encode('ascii', errors='ignore')

lists = re.split(r'\n', raw)
pprint.pprint(lists)

#работающий код
# patterns = ['KLIENT',
#             'ARVE',
#             'Summa KM-ta:',
#             'Kibemaks 20%:',
#             'Kokku:',
#             'Kuupev:',
#             'Maksethtaeg:']
# for l in lists:
#     if any(word in l for word in patterns):
#         print(l)
#конец работающего кода

f = open('../output.txt', 'w')
first_row = ('D' + '\t' + 'kuupaev'.ljust(10) + '\t' + 'maksepaev' + '\t' + 'klient'.ljust(20)
     + '\t' + 'arve'.center(8) + '\t' + 'kokku'.center(9) + '\t' + 'kaibemaks'.center(7) + '\t' + 'KMta'.ljust(7) + '\n')
f.write(first_row)
print(first_row)


Skta = 0.00
Skm = 0.00
Skokk = 0.00

diffDate = ''
klient = ''
summaKMta = 0.00
kibemaks = 0.00
kokku = 0.00
kuupaev = ''
maksepaev = ''

for l in lists:

    if 'KLIENT' in l:
        klient = l.split(':')[1]
        if 'OU,' in klient or 'AS,' in klient or re.search(r'^KLIENT:\s((OU|AS)\s.*)', l):
            klient = klient.split(',')[0]
        elif re.search(r'\s{2,}', l):
            l = re.search(r'KLIENT: (.*)', l).group(1)
            klient = re.split(r'\s{2,}', l)[0]
        else:
            if re.search(r'^.*(OU|AS)', l):
                klient = re.search(r'^KLIENT: (.*(OU|AS))', l).group(1)
        klient = klient[0:24].lstrip().ljust(25)


    if 'ARVE' in l:
        arve = re.search(r'(\d+)', l).group(1)

    if 'Summa KM-ta:' in l:
        summaKMta = re.search(r'(\d+,\d+)', l).group(1)
        summaKMta = summaKMta.rjust(9)
        Skta = Skta + str_to_float(summaKMta)

    if ('Kaibemaks 20%:' in l) or ('Käibemaks 20%:' in l):
        kibemaks = re.search(r'(\d+,\d+)', l).group(1)
        kibemaks = kibemaks.rjust(7)
        Skm = Skm + str_to_float(kibemaks)

    if 'Kokku:' in l:
        kokku = re.search(r'(\d+,\d+)', l).group(1)
        kokku = kokku.rjust(9)
        Skokk = Skokk + str_to_float(kokku)

    if 'Kuupaev:' in l:
        kuupaev = l.strip().replace(' ', '')[8:18]
        maksepaev = l.strip().replace(' ', '')[-13:-3]

        d1 = datetime.datetime.strptime(kuupaev, '%d.%m.%Y')
        try:
            d2 = datetime.datetime.strptime(maksepaev, '%d.%m.%Y')
            diffDate = str(d2 - d1).split(',')[0].split(' ')[0]
        except ValueError:
            diffDate = ''
            klient = ''
            summaKMta = 0.00
            kibemaks = 0.00
            kokku = 0.00
            kuupaev = ''
            maksepaev = ''

        #print(diffDate)


        tt = str(diffDate) + '\t' + kuupaev + '\t' + maksepaev + '\t' + klient +\
                 '\t' + arve + '\t'  + kokku + '\t' + kibemaks + '\t'  + summaKMta

        print(tt)

        diffDate = ''
        klient = ''
        summaKMta = ''
        kibemaks = ''
        kokku = ''
        kuupaev = ''
        maksepaev = ''

        f.write(tt + '\n')

t_it = '\n'+''.rjust(3) +'\t' +''.rjust(10) +'\t' +''.rjust(10)+'\t' +''.rjust(20) +'\t' +''.rjust(6)+'\t' \
       + '\t'+str(format(Skokk, '.2f')).rjust(9) + '\t' + str(format(Skm, '.2f')).rjust(7) \
       + '\t' + str(format(Skta, '.2f')).rjust(9)

print(t_it)
f.write(t_it + '\n')
f.close()
