#чтение счетов Bonus из всей папки в таблицу
#from tika import parser

import datetime


import os
import re
import codecs
import PyPDF2

os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'

import tika
from tika import parser

import re




your_target_folder = "/Users/docha/Google Диск/Bonus/2021-06/"

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

    for pageNum in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)


        pdfWriter.addPage(pageObj)



pdfOutput = open('merged.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()


raw = parser.from_file("/Users/docha/PycharmProjects/Tools_for_buh/merged.pdf")
raw=raw['content']
raw = str(raw)

safe_text = raw.encode('ascii', errors='ignore')
#safe_text = raw.encode('utf-8', errors='ignore').decode('utf-8')
lists = str(safe_text).split("\\n")
#print(lists)

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

f = open('output.txt', 'w')
first_row = ('D' + '\t' + 'kuupaev'.ljust(10) + '\t' + 'maksepaev' + '\t' + 'klient'.ljust(20)
     + '\t' + 'arve'.center(8) + '\t' + 'kokku'.center(9) + '\t' + 'kibemaks'.center(7) + '\t' + 'KMta'.ljust(7) + '\n')
f.write(first_row)
print(first_row)

Skta = 0.00
Skm = 0.00
Skokk = 0.00


for l in lists:
    if 'KLIENT' in l:
        #print(l)
        klient = l.split(':')[1].split(',')[0][0:20]
        klient = klient.lstrip().ljust(20)

    if 'ARVE' in l:
        arve = l.strip()[-8:]

    if 'Summa KM-ta:' in l:
        summaKMta = l.strip().replace(' ','')[11:]
        summaKMta = summaKMta.rjust(9)
        Skta = Skta + float(str(summaKMta).replace(',','.').strip())

    if 'Kibemaks 20%:'in l:
        kibemaks = l.strip().replace(' ','')[12:]
        kibemaks = kibemaks.rjust(7)
        Skm = Skm + float(str(kibemaks).replace(',','.').strip())

    if 'Kokku:' in l:
        kokku = l.strip().replace(' ', '')[6:]
        kokku = kokku.rjust(9)
        Skokk = Skokk + float(str(kokku).replace(',','.').strip())

    if 'Kuupev:' in l:
        kuupaev = l.strip().replace(' ', '')[7:17]
        maksepaev = l.strip().replace(' ','')[-13:-3]

        d1 = datetime.datetime.strptime(kuupaev, '%d.%m.%Y')
        try:
            d2 = datetime.datetime.strptime(maksepaev, '%d.%m.%Y')
            diffDate = str(d2 - d1).split(',')[0].split(' ')[0]
        except ValueError:
            diffDate = ''
            klient = ''
            summaKMta = ''
            kibemaks = ''
            kokku = ''
            kuupaev = ''
            maksepaev = ''

        # print(diffDate)

        tt = str(diffDate) + '\t' + kuupaev + '\t' + maksepaev + '\t' + klient +\
             '\t' + arve + '\t'  + kokku + '\t' + kibemaks + '\t'  + summaKMta

        print(tt)

        f.write(tt + '\n')

t_it = '\n'+''.rjust(3) +'\t' +''.rjust(10) +'\t' +''.rjust(10)+'\t' +''.rjust(20) +'\t' +''.rjust(6)+'\t' \
       + '\t'+str(format(Skokk, '.2f')).rjust(9) + '\t' + str(format(Skm, '.2f')).rjust(7) \
       + '\t' + str(format(Skta, '.2f')).rjust(9)

print(t_it)
f.write(t_it + '\n')
f.close()
