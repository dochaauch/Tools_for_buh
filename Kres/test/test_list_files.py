import os
from unittest import TestCase, mock
from List_files import list_files  # Ensure to import the list_files function correctly


class TestListFiles(TestCase):
    @mock.patch('os.walk')
    def test_list_files_with_matching_extensions(self, mock_walk):
        # Simulate os.walk
        mock_walk.return_value = [
            ('/path', ('dir1',), ('file1.jpg', 'file2.pdf', 'file3.txt')),
            ('/path/dir1', (), ('file4.jpg', 'file5.doc')),
        ]

        expected_files = ['file1.jpg', 'file2.pdf', 'file4.jpg']
        directory = '/path'
        extensions = ('.jpg', '.pdf')

        with mock.patch('builtins.print') as mock_print:
            list_files(directory, extensions)
            mock_print.assert_has_calls([mock.call(file) for file in expected_files])

    @mock.patch('os.walk')
    def test_list_files_with_no_matching_extensions(self, mock_walk):
        # Simulate os.walk with files that do not match the extensions
        mock_walk.return_value = [
            ('/path', ('dir1',), ('file1.txt', 'file2.doc')),
        ]

        directory = '/path'
        extensions = ('.jpg', '.pdf')

        with mock.patch('builtins.print') as mock_print:
            list_files(directory, extensions)
            mock_print.assert_not_called()

    @mock.patch('os.walk')
    def test_list_files_empty_directory(self, mock_walk):
        # Simulate an empty directory
        mock_walk.return_value = []

        directory = '/empty_path'
        extensions = ('.jpg', '.pdf')

        with mock.patch('builtins.print') as mock_print:
            list_files(directory, extensions)
            mock_print.assert_not_called()