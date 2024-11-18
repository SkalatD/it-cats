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
    headers = {"Content-Type": "multipart/form-data"}
    yield api_client(headers=headers, api_key=True)

def test_images_upload(client_key, get_test_image) -> None:
    """ Test that image uploads successfully """
    log.info("Testing - upload test image")
    image_content = get_test_image(image_file="kitty.jpg")
    form_data = {
        "file": image_content,
        "sub_id": "dariia_qa"
    }
    response = client_key.post(endpoint="/images/upload", data=form_data)
    assert response.status_code == 201
