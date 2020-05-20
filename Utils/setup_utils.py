import argparse
import tempfile
import shutil
import os
from pathlib import Path
from datetime import datetime


def setup_dir(dir_path: str):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def create_temp_dir(prefix: str = 'fmpcloud-data') -> str:
    return tempfile.mkdtemp(prefix=prefix)


def rm_dir(dir_path: str) -> bool:
    shutil.rmtree(dir_path)
    return not os.path.exists(dir_path)


def setup_args() -> dict:
    description = 'Script to fetch and parse Edgar 10-Q and 10-K financial statements.'
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
    raw_dir = create_temp_dir()
    data_dir = f'data'
    setup_dir(data_dir)

    args = setup_args()

    return {
        'dirs': {
            'data': data_dir,
            'raw': raw_dir
        },
        'args': args
    }
