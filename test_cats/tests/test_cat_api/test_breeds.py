""" Test file to test The Cat API

NOTE: the api_client fixture is used in this file
Please, see the "conftest.py" file content in order to see the fixture details

To run the tests make sure that pytest is set as a default tests runner in your IDE

"""

import pytest
import logging

log = logging.getLogger(__name__)

@pytest.fixture()
def client_key(api_client):
    log.info("Getting API client with API key provided")
    headers = {"Content-Type": "application/json"}
    yield api_client(headers=headers, api_key=True)

def test_breeds(client_key) -> None:
    """ Test breeds endpoint """
    log.info("Testing - get breeds")
    payload = {"limit": 15}
    response = client_key.get(endpoint="/breeds", params=payload)
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 15
    for breed in response_data:
        assert breed.get("id")
        assert breed.get("name")
        assert breed.get("description")
