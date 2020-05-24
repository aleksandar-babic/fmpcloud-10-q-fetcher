import pathlib

import yaml


class ConfigNotFoundError(Exception):
    pass


class UserConfigParser:
    def __init__(self, config_path: str):
        self.path = config_path
        self.parsed = {}

        if not self._check_config_exists():
            raise ConfigNotFoundError(f'Config at path {self.path} does not exist.')

        self._read_config()

    def _check_config_exists(self) -> bool:
        return pathlib.Path(self.path).is_file()

    def _read_config(self):
        with open(self.path) as f:
            self.raw_config = f.read()

    def get_parsed(self) -> dict:
        if len(self.parsed) == 0:
            self.parsed = yaml.safe_load(self.raw_config)

        return self.parsed
