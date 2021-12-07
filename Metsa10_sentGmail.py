#отправка счетов квартирам на электронные адреса
import yagmail
import csv
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import confid


prefix = '2111'
body = "Arve on lisatud. Счет в приложении"

# перебор файла
with open('name.csv') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        receiver = row['email']
        nr_kor = row['korter']
        subj = 'Metsa 10-{}, arve'.format(nr_kor)


        pdf_document = '/Users/docha/Dropbox/arhiiv_arve_byuh/Metsa10/{}_Metsa10.pdf'.format(prefix)

        pdf = PdfFileReader(pdf_document)

        page = int(row['page'])
        pdf_writer = PdfFileWriter()
        current_page = pdf.getPage(page)
        pdf_writer.addPage(current_page)

        outputFilename = '/Users/docha/Downloads/{}_Metsa10-{}.pdf'.format(prefix, nr_kor)
        with open(outputFilename, 'wb') as out:
            pdf_writer.write(out)
            print('created', outputFilename)


        yag = yagmail.SMTP(user=confid.user, password=confid.password,
                           host='smtp.gmail.com')
                            #использует пароль приложения, двухфакторная аутентификация
        yag.send(
            to=receiver,
            bcc='mob37256213753@gmail.com',
            subject=subj,
            contents=body,
            attachments=outputFilename,
                )

        os.remove(outputFilename)


