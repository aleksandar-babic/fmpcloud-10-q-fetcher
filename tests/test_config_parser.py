import pytest

from UserConfigParser import UserConfigParser, ConfigNotFoundError


class TestConfigParser:

    @pytest.fixture
    def empty_config_file_path(self):
        name = 'empty_config.yml'

        with open(name, 'w') as f:
            f.write('')

        return name

    def test_check_config_exists(self, fs, empty_config_file_path):
        fake_config = UserConfigParser(empty_config_file_path)

        assert fake_config.path == empty_config_file_path

    def test_check_config_exists_not_found(self, fs):
        with pytest.raises(ConfigNotFoundError):
            UserConfigParser('non_existing_config.yml')

    def test_read_config(self, fs, empty_config_file_path):
        raw_config = UserConfigParser(empty_config_file_path).raw_config

        assert raw_config == ''

    def test_parse(self):
        FIXTURE_CONFIG = 'tests/fixtures/config.yml'

        expected_config = {
            'tickers': [
                {
                    'name': 'AAPL',
                    'start_range': 2015,
                    'end_range': 2020
                },
                {
                    'name': 'HUBS',
                    'start_range': 2019,
                    'end_range': 2020
                }
            ]
        }
        actual_config = UserConfigParser(FIXTURE_CONFIG).get_parsed()

        assert expected_config == actual_config

    def test_parse_cache(self):
        FIXTURE_CONFIG = 'tests/fixtures/config.yml'

        parser = UserConfigParser(FIXTURE_CONFIG)

        # First time when get_parsed is called, PyYAML will actually parse the config,
        # Second time, it should just retrieve it from the object instance.
        cache_miss = parser.get_parsed()
        cache_hit = parser.get_parsed()

        assert cache_miss == cache_hit
