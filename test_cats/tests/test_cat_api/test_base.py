""" Test file to test The Cat API

NOTE: the api_client fixture is used in this file
Please, see the "conftest.py" file content in order to see the fixture details

To run the tests make sure that pytest is set as a default tests runner in your IDE

"""

from pytest import mark
import logging

log = logging.getLogger(__name__)

@mark.parametrize("api_key", [None, True])
def test_cat_api_opens(api_client, api_key) -> None:
    """ Test that 'The Cat API' opens with 200 status code with or without API key provided """
    if not api_key:
        log.info("Testing base URL endpoint with no API key")
    else:
        log.info("Testing base URL endpoint with API key provided")

    client = api_client(api_key=api_key)
    response = client.get()  # Testing base URL endpoint
    response_data = response.json()

    assert isinstance(response_data, dict)
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/json; charset=utf-8"
    assert all (key in response_data for key in ["message", "version"])
    assert response_data.get("message") == "The Cat API"
    assert response_data.get("version")
