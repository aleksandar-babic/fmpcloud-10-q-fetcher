import logging
import sys
import re
from os import environ, listdir, path
from zipfile import ZipFile
from pathlib import Path
from datetime import datetime


def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    return logger


def safe_get_env_var(env_var: str) -> str:
    key = environ.get(env_var)

    if key is None:
        raise ValueError(f'{env_var} is required. Set it as environment variable!')

    return key


def save_bytes_to_file(buff_content: bytes, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(buff_content)


def unzip_pwd(zip_path: str) -> str:
    path_wo_extension = Path(zip_path).with_suffix('')

    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(path=path_wo_extension)

    return path_wo_extension


def get_date_from_filename(initial: str) -> str:
    return re.search(r'([0-9]{4}-[0-9]{2}-[0-9]{2})', initial).group(1)


def is_date_in_range(date: str, start_range: int, end_range: int) -> bool:
    date_year = int(date.split('-')[0])

    return start_range <= date_year <= end_range


def is_filename_match(exclude_rules: list, endswith_rules: list, filename: str) -> bool:
    if any(rule in filename for rule in exclude_rules) or \
            all(not filename.endswith(rule) for rule in endswith_rules):
        return False

    return True


def generate_target_filenames(source_directory: str, start_range: int, end_range: int) -> list:
    target_files = []
    for filename in listdir(source_directory):
        if not is_filename_match(['10-K'], ['.xlsx', '.xls'], filename):
            continue

        file = path.join(source_directory, filename)

        filename_only_date = get_date_from_filename(filename)

        if (start_range == 0 and end_range == 0) or \
                is_date_in_range(filename_only_date, start_range, end_range):
            target_files.append({
                'path': file,
                'date': filename_only_date
            })

    target_files.sort(key=lambda curr: datetime.strptime(curr['date'], '%Y-%m-%d'))
    return target_files
