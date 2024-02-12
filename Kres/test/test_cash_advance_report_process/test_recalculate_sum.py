import unittest
from unittest.mock import patch
from Kres.cash_advance_report_process import recalculate_sum


class TestRecalculateSum(unittest.TestCase):
    @patch('Kres.cash_advance_report_process.correct_values')
    def test_recalculate_sum_with_tax_and_total(self, mock_correct_values):
        document_start_index = 0
        km_o_total_for_row = 10.0
        recalculate_tax_and_total = True
        row = {'km': 10.0, 'summa kokku': 20.0}
        zagruzka_data = [{'Сумма с НСО': '10.0'}, {'Сумма с НСО': '10.0'}]

        recalculate_sum(document_start_index, km_o_total_for_row, recalculate_tax_and_total, row, zagruzka_data)

        self.assertEqual(mock_correct_values.call_count, 0)

    @patch('Kres.cash_advance_report_process.correct_values')
    def test_recalculate_sum_with_incorrect_tax(self, mock_correct_values):
        document_start_index = 0
        km_o_total_for_row = 10.0
        recalculate_tax_and_total = True
        row = {'km': 15.0, 'summa kokku': 20.0}
        zagruzka_data = [{'Сумма с НСО': '10.0'}, {'Сумма с НСО': '10.0'}]

        recalculate_sum(document_start_index, km_o_total_for_row, recalculate_tax_and_total, row, zagruzka_data)

        mock_correct_values.assert_called_once_with(zagruzka_data, document_start_index, km_o_total_for_row, row, 'Сумма НСО', 'km', "Старый налог")

    @patch('Kres.cash_advance_report_process.correct_values')
    def test_recalculate_sum_with_incorrect_total(self, mock_correct_values):
        document_start_index = 0
        km_o_total_for_row = 10.0
        recalculate_tax_and_total = True
        row = {'km': 10.0, 'summa kokku': 25.0}
        zagruzka_data = [{'Сумма с НСО': '10.0'}, {'Сумма с НСО': '10.0'}]

        recalculate_sum(document_start_index, km_o_total_for_row, recalculate_tax_and_total, row, zagruzka_data)

        mock_correct_values.assert_called_once_with(zagruzka_data, document_start_index, 20.0, row, 'Сумма с НСО', 'summa kokku', "Старая сумма")

    def test_recalculate_sum_without_tax_and_total(self):
        document_start_index = 0
        km_o_total_for_row = 10.0
        recalculate_tax_and_total = False
        row = {'km': 10.0, 'summa kokku': 20.0}
        zagruzka_data = [{'Сумма с НСО': '10.0'}, {'Сумма с НСО': '10.0'}]

        recalculate_sum(document_start_index, km_o_total_for_row, recalculate_tax_and_total, row, zagruzka_data)

        self.assertEqual(zagruzka_data, [{'Сумма с НСО': '10.0'}, {'Сумма с НСО': '10.0'}])


class TestRecalculateSum(unittest.TestCase):
    def test_recalculate_sum_with_correction(self):
        # Тестовые данные
        zagruzka_data = [
            {'Сумма с НСО': '100.00'},
            {'Сумма с НСО': '200.00'}
        ]
        row = {'km': 150.00, 'summa kokku': 350.00, 'arve nr': '123', 'firma': 'Test Company'}

        print("До коррекции:", zagruzka_data)

        # Вызываем функцию с условием, что пересчет необходим
        recalculate_sum(0, 150.00, True, row, zagruzka_data)

        print("После коррекции:", zagruzka_data)

        # Проверяем, что значения были скорректированы
        self.assertEqual(zagruzka_data[1]['Сумма с НСО'],
                         '250.00')  # Предполагаем, что коррекция была применена к последнему элементу

    def test_recalculate_sum_without_correction_needed(self):
        # Тестовые данные для сценария без коррекции
        zagruzka_data = [
            {'Сумма с НСО': '150.00'},
            {'Сумма с НСО': '200.00'}
        ]
        row = {'km': 150.00, 'summa kokku': 350.00, 'arve nr': '456', 'firma': 'Another Company'}
        initial_data_copy = [row.copy() for row in zagruzka_data]  # Копия исходных данных для сравнения

        print("До попытки коррекции (не требуется):", zagruzka_data)
        recalculate_sum(0, 150.00, True, row, zagruzka_data)
        print("После попытки коррекции (не требуется):", zagruzka_data)

        # Проверяем, что значения не изменились, так как коррекция не требовалась
        self.assertEqual(zagruzka_data, initial_data_copy)

if __name__ == '__main__':
    unittest.main()
