import os
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_single_jpeg(pdf_path, output_folder):
    """Конвертирует PDF в один JPEG, объединяя все страницы."""
    print(f'Обрабатывается файл: {pdf_path}')
    images = convert_from_path(pdf_path)

    # Вычисляем общую высоту всех изображений
    total_height = sum(image.height for image in images)
    max_width = max(image.width for image in images)

    # Создаем новое изображение с подходящими размерами
    combined_image = Image.new('RGB', (max_width, total_height))

    # Склеиваем изображения в одно
    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height

    # Сохраняем результат
    output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(pdf_path))[0] + '.jpg')
    combined_image.save(output_file, 'JPEG')
    print(f'Сохранено: {output_file}')

def main():
    """Основная функция для преобразования всех PDF в папке."""
    #folder_path = '/Users/docha/Library/CloudStorage/GoogleDrive-kres.auto79@gmail.com/Мой диск/2024-02/avansi_val'  # Замените на путь к вашей папке
    #folder_path = '/Users/docha/Library/CloudStorage/GoogleDrive-kres.auto79@gmail.com/Мой диск/2024-04/avansiaruanned'  # Замените на путь к вашей папке
    folder_path = '/Users/docha/Library/CloudStorage/GoogleDrive-kres.auto79@gmail.com/Мой диск/2024-04/avansi_val'  # Замените на путь к вашей папке
    print(f'Начинается обработка папки: {folder_path}')

    for file in os.listdir(folder_path):
        if file.endswith('.pdf') or file.endswith('.PDF'):
            pdf_path = os.path.join(folder_path, file)
            convert_pdf_to_single_jpeg(pdf_path, folder_path)

    print('Обработка завершена.')

if __name__ == "__main__":
    main()

