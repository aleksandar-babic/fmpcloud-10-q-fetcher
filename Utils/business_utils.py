import pandas as pd

from FMPCloudApiClient import FMPCloudApiClient
from .utils import save_bytes_to_file, generate_target_filenames


def save_raw_stmnts(directory: str, ticker: str, api_key: str) -> str:
    client = FMPCloudApiClient(api_key)

    res_bytes = client.fetch_financial_stmnts_zip(ticker)
    target_path = f'{directory}/{ticker}.zip'
    save_bytes_to_file(res_bytes, target_path)

    return target_path


def merge_excel(source_directory: str, target_dir: str, config: dict) -> dict:
    files = generate_target_filenames(source_directory, config['start_date'], config['end_date'])
    start_year = files[0]['date'].split('-')[0]
    end_year = files[-1]['date'].split('-')[0]
    out_path = f"{target_dir}/{config['ticker']}({start_year}-{end_year}).xlsx"

    with pd.ExcelWriter(out_path) as writer:
        for file in files:
            pd.read_excel(file['path']) \
                .to_excel(writer, sheet_name=file['date'], index=False, header=False)

    return {
        'path': out_path,
        'range': f'{start_year}-{end_year}'
    }
