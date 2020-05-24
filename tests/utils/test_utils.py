from os import environ
from time import time
from unittest.mock import patch, mock_open

import pytest

from financestatements.Utils import *


class TestUtils:

    @pytest.fixture
    def env_var(self):
        environ['PYTEST_SAFE_GET_ENV_VAR'] = 'some_value'
        yield 'PYTEST_SAFE_GET_ENV_VAR'
        del environ['PYTEST_SAFE_GET_ENV_VAR']

    def test_safe_get_env_var(self, env_var):
        expected_value = 'some_value'

        assert safe_get_env_var(env_var) == expected_value

    def test_safe_get_env_var_missing(self, env_var):
        with pytest.raises(ValueError):
            safe_get_env_var(f'unexisting_env_variable_{int(time())}')

    def test_save_bytes_to_file(self):
        fake_file_path = "fake/path/file.zip"
        fake_content = b"Mocked Content"

        with patch('builtins.open', mock_open()) as mocked_file:
            save_bytes_to_file(fake_content, fake_file_path)
            mocked_file.assert_called_once_with(fake_file_path, 'wb')
            mocked_file().write.assert_called_once_with(fake_content)

    def test_get_date_from_filename(self):
        fake_file_name = 'SOME_SUPER_IMPORATNT_FILE_2020-05-01-2020-06-01.xlsx'
        expected_date = '2020-05-01'

        assert get_date_from_filename(fake_file_name) == expected_date

    def test_get_date_from_filename_none(self):
        fake_file_name = 'SOME_SUPER_IMPORATNT_FILE.xlsx'

        assert get_date_from_filename(fake_file_name) is None

    def test_is_date_in_range(self):
        date = '2020-05-01'
        start_range = 2019
        end_range = 2021

        assert is_date_in_range(date, start_range, end_range) is True

    def test_is_date_in_range_false(self):
        date = '2018-05-01'
        start_range = 2019
        end_range = 2021

        assert is_date_in_range(date, start_range, end_range) is False

    def test_is_date_in_range_invalid(self):
        with pytest.raises(ValueError) as err:
            date = 'invalid-date'
            start_range = 2019
            end_range = 2021

            is_date_in_range(date, start_range, end_range)

    def test_is_filename_match_exclude_rules(self):
        exclude_rules = ['EXCLUDEME']
        endswitch_rules = []
        filename = 'EXCLUDEME_super_secret.xlsx'

        assert is_filename_match(exclude_rules, endswitch_rules, filename) is False

    def test_is_filename_match_exclude_rules_multiple(self):
        exclude_rules = ['EXCLUDEME', 'EXCLUDEME2']
        endswitch_rules = []
        filename = 'EXCLUDEME_super_secret_EXCLUDEME2.xlsx'

        assert is_filename_match(exclude_rules, endswitch_rules, filename) is False

    def test_is_filename_match_endswith_rules(self):
        exclude_rules = []
        endswitch_rules = ['.pdf']
        filename = 'super_secret.pdf'

        assert is_filename_match(exclude_rules, endswitch_rules, filename) is True

    def test_is_filename_match_endswith_rules_multiple(self):
        exclude_rules = []
        endswitch_rules = ['.xlsx', '.xls']
        filename = 'super_secret.xlsx'
        filename_xls = 'super_secret.xls'

        assert is_filename_match(exclude_rules, endswitch_rules, filename) is True
        assert is_filename_match(exclude_rules, endswitch_rules, filename_xls) is True

    def test_is_filename_match_endswith_rules_false(self):
        exclude_rules = []
        endswitch_rules = ['.pdf']
        filename = 'super_secret.docx'

        assert is_filename_match(exclude_rules, endswitch_rules, filename) is False

    def test_generate_target_filenames(self, mocker):
        source_dir = 'fake/path'
        start_range = 2015
        end_range = 2020
        fake_file_paths = [
            '/fake/path/file1_2020-05-01.xlsx',
            '/fake/path/file1_2020-05-02.xlsx',
            '/fake/path/file1_2020-05-03.xlsx',
            '/fake/path/file1_2010-05-01.xlsx',
            '/fake/path/file1_2012-05-01.xlsx',
            '/fake/path/file1_2015-05-04.xlsx',
            '/fake/path/file1_2018-05-05.xlsx'
        ]

        mocker.patch('os.listdir', return_value=fake_file_paths)

        files = generate_target_filenames(source_dir, start_range, end_range)

        assert len(files) == 5
        assert all('path' in file and 'date' in file for file in files)
        assert all(file['date'] == file['path'].split('file1_')[1].strip('.xlsx') for file in files)

    def test_generate_target_filenames_exclude_pdf(self, mocker):
        source_dir = 'fake/path'
        start_range = 2015
        end_range = 2020
        fake_file_paths = [
            '/fake/path/file1_2020-05-01.xlsx',
            '/fake/path/file1_2020-05-02.xlsx',
            '/fake/path/file1_2020-05-03.xlsx',
            '/fake/path/file1_2010-05-01.xlsx',
            '/fake/path/file1_2012-05-01.xlsx',
            '/fake/path/file1_2015-05-04.pdf',
            '/fake/path/file1_2018-05-05.xlsx'
        ]

        mocker.patch('os.listdir', return_value=fake_file_paths)

        files = generate_target_filenames(source_dir, start_range, end_range)

        assert len(files) == 4
        assert all('path' in file and 'date' in file for file in files)
        assert all(file['date'] == file['path'].split('file1_')[1].strip('.xlsx') for file in files)
