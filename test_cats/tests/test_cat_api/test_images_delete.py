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

def test_images_delete_not_from_account(client_key) -> None:
    """ Test that user cannot delete image not from his account """
    response = client_key.get(endpoint="/images/search", params={"has_breeds": True})
    response_data = response.json()
    image_to_delete = response_data[0]
    image_id = image_to_delete.get("id")
    breed_id = image_to_delete.get("breeds")[0].get("id")
    log.info(f"Testing - delete image with id {image_id} and breed_id {breed_id} not from user account")
    delete_response = client_key.delete(endpoint=f"/images/{image_id}/breeds/{breed_id}")
    expected_text = "AUTHENTICATION_ERROR - you can only edit the breed for images belonging to your account"
    assert delete_response.status_code == 401
    assert delete_response.text == expected_text


