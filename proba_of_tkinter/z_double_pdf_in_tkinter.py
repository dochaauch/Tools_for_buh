import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import fitz

class PDFViewer(ScrolledText):
    def show(self, pdf_file):
        self.delete('1.0', 'end') # clear current content
        pdf = fitz.open(pdf_file) # open the PDF file
        self.images = []   # for storing the page images
        for page in pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = tk.PhotoImage(data=pix1.tobytes('ppm'))
            # insert into the text box
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            # save the image to avoid garbage collected
            self.images.append(photo)

root = tk.Tk()
root.rowconfigure((0,1), weight=1)
root.columnconfigure((0,1), weight=1)

pdf1 = PDFViewer(root, width=80, height=30, spacing3=5, bg='blue')
pdf1.grid(row=0, column=0, sticky='nsew')
pdf1.show('/Users/docha/PycharmProjects/InvoiceNet/train_data/211106_1040_210301_1901_Файл_000 (1).pdf')

pdf2 = PDFViewer(root, width=80, height=30, spacing3=5, bg='blue')
pdf2.grid(row=1, column=1, sticky='nsew')
pdf2.show('FormatForSolvitaNotes.pdf')

root.mainloop()