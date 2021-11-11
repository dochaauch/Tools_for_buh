from PIL import Image

image1 = Image.open(r'/Users/docha/Google Диск/Metsa10/Файл_000.png')
im1 = image1.convert('RGB')
im1.save(r'/Users/docha/Google Диск/Metsa10/Файл_000.pdf')
