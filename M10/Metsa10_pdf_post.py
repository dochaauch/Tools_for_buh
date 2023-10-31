#создание файла для почты (определенные страницы и уменьшен зум)
from PyPDF2 import PdfFileWriter, PdfFileReader

def add_blank_page(writer, unit_size):
    page = writer.addBlankPage(unit_size[0], unit_size[1])
    return page


def scale_to_size(reader, unit_size):
    # Create a writer and populate with pages at unit_size.
    # Scale and merge pages from reader, centered, onto these pages.
    # return open BytesIO object written to by writer

    # For now, just write to aux.pdf

    # determine scaling factor:
    unit_size = reader.pages[3].mediaBox.upperRight


    writer = PdfFileWriter()

    # for in_page in reader.pages:
    for i in range(3, reader.numPages):
        in_page = reader.getPage(i)
        out_page = add_blank_page(writer, unit_size)
        # out_page.mergeScaledPage(in_page, 0.9, expand=True)
        out_page.mergeScaledTranslatedPage(in_page, 0.9, 40, -10, expand=True)


    with open("aux.pdf", "wb") as f:
        writer.write(f)

reader = PdfFileReader(open('/Users/docha/Dropbox/arhiiv_arve_byuh/Metsa10/2309_Metsa10.pdf', 'rb'))

scale_to_size(reader, unit_size=reader.pages[3].mediaBox.upperRight)
