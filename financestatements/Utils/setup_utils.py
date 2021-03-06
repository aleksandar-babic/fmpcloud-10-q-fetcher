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


def get_home_dir() -> str:
    return str(Path.home())


def setup_args() -> dict:
    description = 'Script to fetch and parse Edgar 10-Q and 10-K financial statements.'
    usage = '''
    # Get all available statements
    # Output will be stored in $HOMEDIR/fmpcloud by default
    finance-statements.py --ticker HUBS
    
    # Get all available statements in /home/user/joe/reports (override default output path)
    finance-statements.py --ticker HUBS --output /home/user/joe/reports
    
    # Get all available statements for multiple companies in default location
    finance-statements.py --ticker HUBS,NFLX,AAPL
    
    # Get all available statements for multiple companies from config file
    finance-statements.py --config example_config.yml
    
    # Get statements from 2017 till 2020
    finance-statements.py --ticker HUBS --start 2017 --end 2020
    
    # Get statements from 2017 till 2020 for multiple companies
    finance-statements.py --ticker HUBS,NFLX,AAPL --start 2017 --end 2020
     
    # Get statements from 2017 till present
    finance-statements.py --ticker HUBS --start 2017
    
    # Get statements from oldest till 2018
    finance-statements.py --ticker HUBS --end 2018
    '''
    parser = argparse.ArgumentParser(description=description, usage=usage)
    parser.add_argument('--ticker', type=lambda s: s.split(','),
                        help='Comma delimited list of company tickers.')
    parser.add_argument('--start', type=int, help='Start year of financial statements.', default=0)
    parser.add_argument('--end', type=int, help='End year of financial statements.', default=datetime.now().year)
    parser.add_argument('--config', type=str, help='Path to the company configuration file.')
    parser.add_argument('--output', type=str, help='Path to directory where output will be stored.')
    args = parser.parse_args()
    args_dict = vars(args)

    if args_dict['start'] > args_dict['end']:
        raise ValueError('start range cant be greater than end range.')

    if ('ticker' not in args_dict or args_dict['ticker'] is None) and (
            'config' not in args_dict or args_dict['config'] is None):
        raise ValueError('Either --config or --ticker option is required.')

    return args_dict


def setup() -> dict:
    args = setup_args()

    raw_dir = create_temp_dir()

    DEFAULT_DATA_SUFFIX = 'fmpcloud'
    is_output_set = args.get('output') is not None
    data_dir = args['output'] if is_output_set else f'{str(get_home_dir())}/{DEFAULT_DATA_SUFFIX}'

    setup_dir(data_dir)

    return {
        'dirs': {
            'data': data_dir,
            'raw': raw_dir
        },
        'args': args
    }
