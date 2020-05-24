import os
from unittest import mock
import argparse
import tempfile
from datetime import datetime

import pytest

from Utils import *


class TestSetupUtils:
    def test_setup_dir(self, fs):
        fake_path = '/fake/path/dir'

        assert os.path.exists(fake_path) is False
        setup_dir(fake_path)
        assert os.path.exists(fake_path)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(ticker='NFLX', start=2015, end=2020))
    def test_setup_args(self, mock_args):
        actual_args = setup_args()

        expected_args = {
            'ticker': 'NFLX',
            'start': 2015,
            'end': 2020
        }

        assert actual_args == expected_args

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(ticker='NFLX', start=0, end=datetime.now().year))
    def test_setup_args_defaults(self, mock_args):
        actual_args = setup_args()

        expected_args = {
            'ticker': 'NFLX',
            'start': 0,
            'end': datetime.now().year
        }

        assert actual_args == expected_args

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(ticker='NFLX', start=2018, end=2015))
    def test_setup_args_end_before_start(self, mock_args):
        with pytest.raises(ValueError):
            setup_args()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(start=2015, end=2020))
    def test_setup_args_no_ticker_config(self, mock_args):
        with pytest.raises(ValueError):
            setup_args()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(ticker='NFLX', start=2015, end=2020))
    def test_setup(self, mock_args, fs):
        setup_config = setup()

        actual_raw_path = setup_config['dirs']['raw']
        assert tempfile.gettempdir() in actual_raw_path

        expected_setup_config_without_raw = {
            'dirs': {
                'data': f'{get_home_dir()}/fmpcloud'
            },
            'args': {
                'ticker': 'NFLX',
                'start': 2015,
                'end': 2020
            }
        }

        del setup_config['dirs']['raw']
        assert expected_setup_config_without_raw == setup_config

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    ticker='NFLX',
                    start=2015,
                    end=2020,
                    output=f'{get_home_dir()}/fakefspytestoverride'
                ))
    def test_setup_override_output(self, mock_args, fs):
        setup_config = setup()

        actual_raw_path = setup_config['dirs']['raw']
        assert tempfile.gettempdir() in actual_raw_path

        expected_setup_config_without_raw = {
            'dirs': {
                'data': f'{get_home_dir()}/fakefspytestoverride'
            },
            'args': {
                'ticker': 'NFLX',
                'start': 2015,
                'end': 2020,
                'output': f'{get_home_dir()}/fakefspytestoverride'
            }
        }

        del setup_config['dirs']['raw']
        assert expected_setup_config_without_raw == setup_config

    def test_create_temp_dir(self, fs):
        temp_dir_path = create_temp_dir('pytest-fakefs')
        assert os.path.exists(temp_dir_path)

    def test_rm_dir(self, fs):
        temp_dir_path = create_temp_dir('pytest-fakefs')

        assert rm_dir(temp_dir_path)

    def test_rm_dir_nonexisting(self, fs):
        nonexisting_path = '/tmp/fmpcloudpytest-fakefs-non-existing-dir'
        with pytest.raises(FileNotFoundError):
            rm_dir(nonexisting_path)

    def test_get_home_dir(self):
        expected_home_dir = os.environ.get('HOME')

        assert expected_home_dir is not None
        assert get_home_dir() == expected_home_dir
