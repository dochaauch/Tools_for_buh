#сбор определенного номера страницы со всех файлов из папки из папки

import PyPDF2
import os


your_target_folder = "/Users/docha/PycharmProjects/PageNmPdfInOne"

pdf_files = []

for dirpath, _, filenames in os.walk(your_target_folder):

    for items in filenames:

        file_full_path = os.path.abspath(os.path.join(dirpath, items))

        if file_full_path.lower().endswith(".pdf"):
            pdf_files.append(file_full_path)

        else:
            pass


pdf_files.sort(key=str.lower)
pdfWriter = PyPDF2.PdfFileWriter()



for files_address in pdf_files:
    pdfFileObj = open(files_address, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    list_pages = []
    #input1 = PyPDF2.PdfFileReader(open(src, "rb"))
    nPages = pdfReader.getNumPages()

    #print (nPages)
    for i in range(nPages):
        if i == 25:  #вводим требуемый номер страницы, отсчет начинается с 0
            page0 = pdfReader.getPage(i)
            #print(page0)
            try:
                for annot in page0['/Annots']:
                    list_pages.append(i)
            except:
                # there are no annotations on this page
                pass
    r = set(list_pages)
    for lst in r:
        pageObj = pdfReader.getPage(lst)
        pdfWriter.addPage(pageObj)




with open("CombinedPages.pdf", "wb") as output:
    pdfWriter.write(output)
