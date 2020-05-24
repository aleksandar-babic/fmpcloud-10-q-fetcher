# FMPCloud 10-Q statements fetcher
![cov](.github/coverage_badge.svg)
  
Python script that uses `FMPCloud API` to fetch 10-Q and 10-K statements for given company.

## Usage
```shell script
usage: 
    # Get all available statements
    # Output will be stored in $HOMEDIR/fmpcloud by default
    finance-statements --ticker HUBS
    
    # Get all available statements in /home/user/joe/reports (override default output path)
    finance-statements --ticker HUBS --output /home/user/joe/reports
    
    # Get all available statements for multiple companies in default location
    finance-statements --ticker HUBS,NFLX,AAPL
    
    # Get all available statements for multiple companies from config file
    finance-statements --config example_config.yml
    
    # Get statements from 2017 till 2020
    finance-statements --ticker HUBS --start 2017 --end 2020
    
    # Get statements from 2017 till 2020 for multiple companies
    finance-statements --ticker HUBS,NFLX,AAPL --start 2017 --end 2020
     
    # Get statements from 2017 till present
    finance-statements --ticker HUBS --start 2017
    
    # Get statements from oldest till 2018
    finance-statements --ticker HUBS --end 2018
    

Script to fetch and parse Edgar 10-Q and 10-K financial statements.

optional arguments:
  -h, --help       show this help message and exit
  --ticker TICKER  Comma delimited list of company tickers.
  --start START    Start year of financial statements.
  --end END        End year of financial statements.
  --config CONFIG  Path to the company configuration file.
  --output OUTPUT  Path to directory where output will be stored.
```
> Output will be saved in `$HOME/fmpcloud` by default. To override use `--output`.
  
> Either `--ticker` or `--config` option should be specified, not both. If both specified, config will have priority.
## Setup

### Requirements:
* [FMPCloud API account](https://fmpcloud.io/plans)
* Python 3.8
* Pipenv

### Setup steps:
```shell script
# Install dependencies
pipenv install

# Spawn venv shell
pipenv shell

# Export FMPCloud API key to environment variable
# If you don't have the account yet, use `demo` for api key value
export FMPCLOUD_API_KEY=api_key_value

# Run the script, get statements for all years
python finance-statements --ticker NFLX

# Run the script, get statements for period 2010-2015
python finance-statements --ticker NFLX --start 2010 --end 2015
```
> Transformed resulting report will be saved in the `data` directory.
  
> Optionally, env variable `FMPCLOUD_LOGLEVEL` can be set to value `DEBUG` for more verbose logging.

### Running tests
```shell script
# Install dependencies
pipenv install

# Spawn venv shell
pipenv shell

# Run pytest tests
python -m pytest

# Run pytest tests with coverage
python -m pytest --cov='.' --cov-report=html
```
> HTML coverage reports will be saved in the `htmlcov` directory.

### Configuration file
If you need reports for many companies and/or different time ranges per company, config file is your friend.
  
#### Config content
```yaml
---

tickers:
  -
    name: AAPL
    start_range: 2015
    end_range: 2020
  -
    name: HUBS
    start_range: 2019
    end_range: 2020
```
> Tickers is a list, each item in the list represents one report for the specified company.

#### Config usage
```shell script
python finance-statements --config example_config.yml
```
> Example available in the git repo, named `example_config.yml`.