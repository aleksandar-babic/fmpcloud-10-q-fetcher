import os
from unittest import mock
import argparse
from datetime import datetime

import pytest

from Utils import *


class TestSetupUtils:
    def test_setup_dir(self, fs):
        fake_path = '/fake/path/dir'

        assert os.path.exists(fake_path) is False
        setup_dir(fake_path)
        assert os.path.exists(fake_path)

    def test_setup_base_dirs(self, fs):
        data_dir = 'fake/path/data'
        raw_dir = f'fake/path/raw'

        assert os.path.exists(data_dir) is False
        assert os.path.exists(raw_dir) is False
        setup_base_dirs(data_dir, raw_dir)
        assert os.path.exists(data_dir)
        assert os.path.exists(raw_dir)

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
                return_value=argparse.Namespace(ticker='NFLX', start=2015, end=2020))
    def test_setup(self, fs):
        setup_config = setup()

        expected_setup_config = {
            'dirs': {
                'data': 'data',
                'raw': 'data/.raw'
            },
            'args': {
                'ticker': 'NFLX',
                'start': 2015,
                'end': 2020
            }
        }

        assert setup_config == expected_setup_config
