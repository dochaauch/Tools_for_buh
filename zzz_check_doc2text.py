import doc2text
#import _PythonMagick

# Initialize the class.
doc = doc2text.Document()

# You can pass the lang (as 3 letters code) to the class to improve accuracy
# On ubuntu it requires the package tesseract-ocr-$lang$
# On other OS, see https://github.com/tesseract-ocr/langdata
doc = doc2text.Document(lang="eng")

# Read the file in. Currently accepts pdf, png, jpg, bmp, tiff.
# If reading a PDF, doc2text will split the PDF into its component pages.
doc.read('/Users/docha/Google Диск/Bonus/2021-04/a22_29.04.2021_bonus_tolkeburoo_waved_stripes.pdf')

# Crop the pages down to estimated text regions, deskew, and optimize for OCR.
doc.process()

# Extract text from the pages.
doc.extract_text()
text = doc.get_text()
print(text)
