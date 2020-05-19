import pytest

from FMPCloudApiClient import FMPCloudApiClient


class TestBusinessUtils:
    def test_fetch_financial_stmnts_zip(self, requests_mock):
        api_key = 'demo'
        ticker = 'NFLX'
        client = FMPCloudApiClient(api_key)

        mock_get_url = f"{FMPCloudApiClient.BASE_URL}/" \
                       f"{FMPCloudApiClient.ENDPOINTS['financial_stmnts']}/" \
                       f"{ticker}?datatype=zip&apikey={api_key}"

        mocked_content = 'zipfilecontent'
        requests_mock.get(mock_get_url, status_code=200, text=mocked_content)

        res_content = client.fetch_financial_stmnts_zip(ticker)
        assert res_content == str.encode(mocked_content)

    def test_fetch_financial_stmnts_zip_value_error(self, requests_mock):
        with pytest.raises(ValueError):
            api_key = 'demo'
            ticker = 'NFLXFNOTFOUND'
            client = FMPCloudApiClient(api_key)

            mock_get_url = f"{FMPCloudApiClient.BASE_URL}/" \
                           f"{FMPCloudApiClient.ENDPOINTS['financial_stmnts']}/" \
                           f"{ticker}?datatype=zip&apikey={api_key}"

            requests_mock.get(mock_get_url, status_code=404)

            client.fetch_financial_stmnts_zip(ticker)
