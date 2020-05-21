import os
import pathlib
import pytest

from Utils import *


class TestBusinessUtils:
    @pytest.fixture
    def hubs_zip(self):
        with open('tests/fixtures/HUBS.zip', 'rb') as f:
            return f.read()

    def test_save_raw_stmnts(self, requests_mock, hubs_zip, fs):
        api_key = 'demo'
        dest_dir = create_temp_dir()
        ticker = 'HUBS'

        mock_get_url = f"{FMPCloudApiClient.BASE_URL}/" \
                       f"{FMPCloudApiClient.ENDPOINTS['financial_stmnts']}/" \
                       f"{ticker}?datatype=zip&apikey={api_key}"
        requests_mock.get(mock_get_url, status_code=200, content=hubs_zip)

        expected_path = f'{dest_dir}/{ticker}.zip'
        assert save_raw_stmnts(dest_dir, ticker, api_key) == expected_path

    def test_merge_excel(self, requests_mock, hubs_zip, fs):
        api_key = 'demo'
        dest_dir = create_temp_dir()
        data_dir = create_temp_dir()
        ticker = {
            'name': 'HUBS',
            'start_range': 2014,
            'end_range': 2020
        }

        mock_get_url = f"{FMPCloudApiClient.BASE_URL}/" \
                       f"{FMPCloudApiClient.ENDPOINTS['financial_stmnts']}/" \
                       f"{ticker['name']}?datatype=zip&apikey={api_key}"
        requests_mock.get(mock_get_url, status_code=200, content=hubs_zip)

        zip_path = save_raw_stmnts(dest_dir, ticker['name'], api_key)
        extracted_path = unzip_pwd(zip_path)

        out = merge_excel(extracted_path, data_dir, ticker)

        expected_out = {
            'path': f"{data_dir}/{ticker['name']}({ticker['start_range']}-{ticker['end_range']}).xlsx",
            'range': f"{ticker['start_range']}-{ticker['end_range']}"
        }

        assert out == expected_out

    def test_get_tickers(self):
        args = {
            'ticker': ['AAPL', 'NFLX', 'HUBS'],
            'start': 0,
            'end': 2020,
            'output': None
        }

        tickers = get_tickers(args)

        expected_tickers = [
            {
                'name': 'AAPL',
                'start_range': 0,
                'end_range': 2020
            },
            {
                'name': 'NFLX',
                'start_range': 0,
                'end_range': 2020
            },
            {
                'name': 'HUBS',
                'start_range': 0,
                'end_range': 2020
            }
        ]

        assert tickers == expected_tickers

    def test_process_tickers(self, requests_mock, hubs_zip, fs):
        api_key = 'demo'
        raw_dir = create_temp_dir()
        data_dir = create_temp_dir()
        args = {
            'ticker': ['AAPL', 'NFLX', 'HUBS'],
            'start': 2014,
            'end': 2020,
            'output': None
        }

        for mock_ticker in args['ticker']:
            mock_get_url = f"{FMPCloudApiClient.BASE_URL}/" \
                           f"{FMPCloudApiClient.ENDPOINTS['financial_stmnts']}/" \
                           f"{mock_ticker}?datatype=zip&apikey={api_key}"
            requests_mock.get(mock_get_url, status_code=200, content=hubs_zip)

        tickers = get_tickers(args)
        tickers_config = {
            'api_key': api_key,
            'dirs': {
                'raw': raw_dir,
                'data': data_dir
            },
            'tickers': tickers,
        }

        process_tickers(tickers_config, get_logger())
        for ticker in tickers:
            expected_path = f"{data_dir}/{ticker['name']}({ticker['start_range']}-{ticker['end_range']}).xlsx"
            assert pathlib.Path(expected_path).exists()

    def test_process_tickers_error(self, requests_mock, fs):
        api_key = 'demo'
        raw_dir = create_temp_dir()
        data_dir = '/nonexisting/directory/intentionally/failing'
        args = {
            'ticker': ['AAPL', 'NFLX', 'HUBS'],
            'start': 2014,
            'end': 2020,
            'output': None
        }

        for mock_ticker in args['ticker']:
            mock_get_url = f"{FMPCloudApiClient.BASE_URL}/" \
                           f"{FMPCloudApiClient.ENDPOINTS['financial_stmnts']}/" \
                           f"{mock_ticker}?datatype=zip&apikey={api_key}"
            requests_mock.get(mock_get_url, status_code=500)

        tickers = get_tickers(args)
        tickers_config = {
            'api_key': api_key,
            'dirs': {
                'raw': raw_dir,
                'data': data_dir
            },
            'tickers': tickers,
        }

        process_tickers(tickers_config, get_logger())
        for ticker in tickers:
            expected_path = f"{data_dir}/{ticker['name']}({ticker['start_range']}-{ticker['end_range']}).xlsx"
            assert not pathlib.Path(expected_path).exists()
