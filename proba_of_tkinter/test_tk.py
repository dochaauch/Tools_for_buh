from tkinter import *

from tkPDFViewer import tkPDFViewer as pdf

root = Tk()
root.geometry("550x750")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
frame1 = Frame(root)
frame1.grid(row=0, column=0)
for r in range(3):
   for c in range(4):
      a = Label(frame1, text='R%s/C%s'%(r,c),
         borderwidth=1)
      print(type(a), a)
      a.grid(row=r, column=c)
frame2 = Frame(root)
frame2.grid(row=0, column=1)
v1 = pdf.ShowPdf()
file_ = r'/Users/docha/PycharmProjects/InvoiceNet/train_data/210301_1901_Файл_000 (1).pdf'
v2 = v1.pdf_view(frame2, pdf_location=file_, width=100, height=100, load="")
v2.pack()

root.mainloop()
