# Importing tkinter to make gui in python
import os
from tkinter import *
from PIL import Image as PILImage

# Importing tkPDFViewer to place pdf file in gui.
# In tkPDFViewer library there is
# an tkPDFViewer module. That I have imported as pdf
from tkPDFViewer import tkPDFViewer as pdf


def convert_jpg_to_pdf(file_jpg):
    new_name = os.path.basename(file_jpg).split('.')[0] + '.pdf'
    file_ = PILImage.open(file_jpg).convert('RGB')
    file_.save(os.path.join(os.path.dirname(file_jpg), new_name))
    file_ = os.path.join(os.path.dirname(file_jpg), new_name)
    return file_


def tk_window():
    """
    Initializing tk
    :return:
    """
    root = Tk()

    # Set the width and height of our root window.
    #root.resizable(width=False, height=False)
    root.geometry("1050x550")

    #root.columnconfigure(0, weight=2)
    #root.columnconfigure(1, weight=1)

    #frame_pdf = Frame(root, bg='green',)
    #frame_pdf.grid(row=0, column=0)

    #frame_check = Frame(root, bg='red')
    #frame_check.grid(row=0, column=1)


    # creating object of ShowPdf from tkPDFViewer.
    v1 = pdf.ShowPdf()

    # Adding pdf location and width and height.

    file_jpg = r'/Users/docha/PycharmProjects/InvoiceNet/train_data/210301_1901_Файл_000 (1).jpg'

    file_ = convert_jpg_to_pdf(file_jpg)

    v2 = v1.pdf_view(root,
                     pdf_location=file_,
                     width=100, height=550, load="")
                    #load="" or bar='False'
    # Placing Pdf in my gui.
    v2.grid(row=0, column=1, rowspan=4)
    #v2.grid(row=0, column=1, sticky=W)

    label_test = Label(root, text='Test', bg='red')
    label_test.grid(row=0, column=0, sticky=W)
    #label_test.pack()

    root.mainloop()


def main():
    tk_window()


if __name__ == '__main__':
    main()
