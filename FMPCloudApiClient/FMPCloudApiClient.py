import requests


class FMPCloudApiClient:
    BASE_URL = 'https://fmpcloud.io/api/v3'
    ENDPOINTS = {
        'financial_stmnts': 'financial-statements'
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_financial_stmnts_zip(self, ticker: str) -> bytes:
        params = {
            'datatype': 'zip',
            'apikey': self.api_key
        }

        res = requests.get(f"{self.BASE_URL}/{self.ENDPOINTS['financial_stmnts']}/{ticker}", params=params)

        if res.status_code != 200:
            raise ValueError(f'Unexpected response from the API. Status code: {res.status_code}, Data: {res.text}')

        return res.content
