# FMPCloud 10-Q statements fetcher
![cov](.github/coverage_badge.svg)
  
Python script that uses `FMPCloud API` to fetch 10-Q and 10-K statements for given company.

## Usage
```shell script
usage: 
    # Get all available statements
    # Output will be stored in $HOMEDIR/fmpcloud by default
    main.py --ticker HUBS
    
    # Get all available statements in /home/user/joe/reports (override default output path)
    main.py --ticker HUBS --output /home/user/joe/reports
    
    # Get all available statements for multiple companies in default location
    main.py --ticker HUBS,NFLX,AAPL
    
    # Get statements from 2017 till 2020
    main.py --ticker HUBS --start 2017 --end 2020
    
    # Get statements from 2017 till 2020 for multiple companies
    main.py --ticker HUBS,NFLX,AAPL --start 2017 --end 2020
     
    # Get statements from 2017 till present
    main.py --ticker HUBS --start 2017
    
    # Get statements from oldest till 2018
    main.py --ticker HUBS --end 2018
    

Script to fetch and parse Edgar 10-Q and 10-K financial statements.

optional arguments:
  -h, --help       show this help message and exit
  --ticker TICKER  Comma delimited list of company tickers.
  --start START    Start year of financial statements.
  --end END        End year of financial statements.
  --output OUTPUT  Path to directory where output will be stored.
```
> Output will be saved in `$HOME/fmpcloud` by default. To override use `--output`.

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
python main.py --ticker NFLX

# Run the script, get statements for period 2010-2015
python main.py --ticker NFLX --start 2010 --end 2015
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