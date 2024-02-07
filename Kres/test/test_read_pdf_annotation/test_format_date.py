import unittest
from Kres.read_pdf_annotation import format_date


class TestFormatDate(unittest.TestCase):
    def test_format_date(self):
        # Test with a date string in the format "day month_name year"
        self.assertEqual(format_date("01 jaanuar 2022"), "01.01.2022")
        self.assertEqual(format_date("15 veebruar 2023"), "15.02.2023")
        self.assertEqual(format_date("31 detsember 2024"), "31.12.2024")

        # Test with a date string in the format "day month_name year" with extra spaces
        self.assertEqual(format_date(" 01   jaanuar   2022 "), "01.01.2022")

        # Test with a date string in the format "day.month.year"
        self.assertEqual(format_date("01.01.2022"), "01.01.2022")

        # Test with a date string in the format "day/month/year"
        self.assertEqual(format_date("01/01/2022"), "01.01.2022")

        # Test with a date string in the format "day-month-year"
        self.assertEqual(format_date("01-01-2022"), "01.01.2022")

        # Test with a date string in the format "day month_name year" in English
        self.assertEqual(format_date("01 january 2022"), "01.01.2022")

        # Test with a date string in the format "day month_name year" with mixed case
        self.assertEqual(format_date("01 JaAnUaR 2022"), "01.01.2022")

        # Test with a date string in the format "day month_name year" with invalid month name
        self.assertIsNone(format_date("01 invalid_month 2022"))

        # Test with a date string in the format "day month_name year" with invalid day
        self.assertIsNone(format_date("32 jaanuar 2022"))

        # Test with a date string in the format "day month_name year" with invalid year
        self.assertIsNone(format_date("01 jaanuar 20222"))


if __name__ == '__main__':
    unittest.main()
