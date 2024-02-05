import tabula
# Преобразование PDF в DataFrame
pdf_path = '/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/doki/2022_Bilans_kasum.pdf'
df = tabula.read_pdf(pdf_path, pages='all')[0]
# Сохранение в Excel
df.to_excel('output.xlsx', index=False)
