import unittest
from Kres.cash_advance_report_process import read_excel, create_new_sheet_with_headers


class TestExcelFileReader(unittest.TestCase):
    def setUp(self):
        # Этот метод будет вызываться перед каждым тестом
        self.file_path = "/Kres/test/_svod_2312.xlsx"
        self.sheet_name = "svod"
        self.new_sheet_name = "zagruzka"


    def test_read_excel_file_positive(self):
        data = read_excel(self.file_path, self.sheet_name)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)

    def test_read_excel_file_negative(self):
        file_path = "/path/to/nonexistent/file.xlsx"
        sheet_name = "svod"
        # Check if FileNotFoundError is raised when trying to read a nonexistent file
        with self.assertRaises(FileNotFoundError):
            read_excel(file_path, sheet_name)

    def test_create_new_sheet_with_headers(self):
        headers = [
            'Вид бухгалтерской операции',
            'Счет',
            'Контрагент НСО',
            'Дата документа',
            'Вид документа НСО',
            'Серия документа',
            'Номер документа',
            'Валюта отчета',
            'Курс валюты отчета',
            'Сумма',
            'Ставка НСО',
            'Сумма НСО',
            'Сумма с НСО',
            'Счет проводки НСО',
            'Применение НСО',
            'Аналитика по НСО',
            'Счет 50%',
            'Субконто1',
            'Субконто2',
            'Субконто3',
            'Субконто4',
            'Субконто5',
            'Субконто1 50%',
            'Субконто2 50%',
            'Субконто3 50%',
            'Субконто4 50%',
            'Субконто5 50%',
            'Основание',
            'Комментарий',
        ]  # Все 29 заголовков
        create_new_sheet_with_headers(self.file_path, self.new_sheet_name, headers)
        data = read_excel(self.file_path, self.new_sheet_name)
        self.assertEqual(list(data[0]), headers)  # Проверяем, что заголовки есть