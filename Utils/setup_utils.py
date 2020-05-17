import argparse
from pathlib import Path
from datetime import datetime


def setup_base_dirs(data_dir: str, raw_dir: str):
    setup_dir(data_dir)
    setup_dir(raw_dir)


def setup_dir(dir_path: str):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def setup_args() -> dict:
    description = 'Script to fetch and parse Edgar 10-Q financial statements.'
    usage = '''
    # Get all available statements
    main.py --ticker HUBS
    
    # Get statements from 2017 till 2020
    main.py --ticker HUBS --start 2017 --end 2020
     
    # Get statements from 2017 till present
    main.py --ticker HUBS --start 2017
    
    # Get statements from oldest till 2018
    main.py --ticker HUBS --end 2018
    '''
    parser = argparse.ArgumentParser(description=description, usage=usage)
    parser.add_argument('--ticker', help='Company ticker', required=True)
    parser.add_argument('--start', type=int, help='Start year of financial statements.', default=0)
    parser.add_argument('--end', type=int, help='End year of financial statements.', default=datetime.now().year)
    args = parser.parse_args()
    args_dict = vars(args)

    if args_dict['start'] > args_dict['end']:
        raise ValueError('start range cant be greater than end range.')

    return args_dict


def setup() -> dict:
    DATA_DIR = 'data'
    RAW_DIR = f'{DATA_DIR}/.raw'
    setup_base_dirs(DATA_DIR, RAW_DIR)

    args = setup_args()

    return {
        'dirs': {
            'data': DATA_DIR,
            'raw': RAW_DIR
        },
        'args': args
    }
