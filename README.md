# FMPCloud 10-Q statements fetcher

Python script that uses `FMPCloud API` to fetch 10-Q statements for given company.

## Usage
```shell script
usage: 
    # Get all available statements
    main.py --ticker HUBS
    
    # Get statements from 2017 till 2020
    main.py --ticker HUBS --start 2017 --end 2020
     
    # Get statements from 2017 till present
    main.py --ticker HUBS --start 2017
    
    # Get statements from oldest till 2018
    main.py --ticker HUBS --end 2018
    

Script to fetch and parse Edgar 10-Q financial statements.

optional arguments:
  -h, --help       show this help message and exit
  --ticker TICKER  Company ticker
  --start START    Start year of financial statements.
  --end END        End year of financial statements.
```

## Setup

### Requirements:
* [FMPCloud API Pro account](https://fmpcloud.io/)
* Python 3.8
* Pipenv

### Setup steps:
```shell script
# Export FMPCloud API key to environment variable
export FMPCLOUD_API_KEY=api_key_value

# Install dependencies
pipenv install

# Run the script, get statements for all years
python main.py --ticker NFLX

# Run the script, get statements for period 2010-2015
python main.py --ticker NFLX --start 2010 --end 2015
```
> Transformed resulting report will be saved in the `data` directory.
  
> Directory `data/.raw` contains untransformed data received from the API.