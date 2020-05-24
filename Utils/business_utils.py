import pandas as pd
import logging

from FMPCloudApiClient import FMPCloudApiClient
from UserConfigParser import UserConfigParser
from .utils import save_bytes_to_file, generate_target_filenames, unzip_pwd


def save_raw_stmnts(directory: str, ticker: str, api_key: str) -> str:
    client = FMPCloudApiClient(api_key)

    res_bytes = client.fetch_financial_stmnts_zip(ticker)
    target_path = f'{directory}/{ticker}.zip'
    save_bytes_to_file(res_bytes, target_path)

    return target_path


def merge_excel(source_directory: str, target_dir: str, config: dict) -> dict:
    files = generate_target_filenames(source_directory, config['start_range'], config['end_range'])
    start_year = files[0]['date'].split('-')[0]
    end_year = files[-1]['date'].split('-')[0]
    out_path = f"{target_dir}/{config['name']}({start_year}-{end_year}).xlsx"

    with pd.ExcelWriter(out_path) as writer:
        for file in files:
            pd.read_excel(file['path']) \
                .to_excel(writer, sheet_name=file['date'], index=False, header=False)

    return {
        'path': out_path,
        'range': f'{start_year}-{end_year}'
    }


def get_tickers(args: dict) -> list:
    if 'config' in args and args['config'] is not None:
        config = UserConfigParser(args['config']).get_parsed()
        if 'tickers' not in config:
            raise ValueError('Invalid config file content. Expected key `tickers`.')

        return config['tickers']

    return [{
        'name': ticker,
        'start_range': args['start'],
        'end_range': args['end']
    } for ticker in args['ticker']]


def process_tickers(config: dict, logger: logging.Logger):
    for ticker in config['tickers']:
        try:
            zip_path = save_raw_stmnts(config['dirs']['raw'], ticker['name'], config['api_key'])
            extracted_path = unzip_pwd(zip_path)
            logger.debug(f'Saved raw financial statements in {extracted_path}.')

            out = merge_excel(extracted_path, config['dirs']['data'], ticker)
            logger.info(f"Saved financial statements for {ticker['name']}({out['range']}) in {out['path']}.")
        except Exception as e:
            logger.info(f'Failed to process ticker {ticker}. Error:{e}')
