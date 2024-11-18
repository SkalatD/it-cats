""" Test file to test The Cat API

NOTE: the api_client fixture is used in this file
Please, see the "conftest.py" file content in order to see the fixture details

To run the tests make sure that pytest is set as a default tests runner in your IDE

"""

import pytest
import logging
import re

log = logging.getLogger(__name__)
# Image keys
image_object_keys = ["id", "url", "width", "height"]
# Regex pattern for valid image/animation URLs
image_url_pattern = re.compile(
        pattern=r'^https://.*\.(jpg|jpeg|png|gif|bmp|webp|svg|tiff|tif|apng|ico)$',
        flags=re.IGNORECASE  # Case-insensitive for file extensions
    )

@pytest.fixture()
def client_key(api_client):
    log.info("Getting API client with API key provided")
    yield api_client(api_key=True)

def test_search_random_image_key(client_key) -> None:
    """ Test that images/search endpoint returns image info """
    log.info("Testing - search random image with provided API key")
    response = client_key.get(endpoint="/images/search")  # Testing images/search endpoint
    response_data = response.json()
    image = response_data[0]
    assert response.status_code == 200
    assert isinstance(response_data, list)
    assert isinstance(image, dict)
    assert response.headers.get("Content-Type") == "application/json; charset=utf-8"
    assert all(image.get(key) for key in image_object_keys)
    assert image_url_pattern.match(str(image.get("url")))
    image_width = image.get("width")
    image_height = image.get("height")
    assert isinstance(image_width, int) and image_width > 0
    assert isinstance(image_height, int) and image_height > 0
    assert len(response_data) == 1

@pytest.mark.parametrize("number_images", [11, 25, 50, 100])
def test_search_up_to_100_images_key(client_key, number_images) -> None:
    """ Test that searching up to 100 images is successful with API key """
    payload = {"limit": number_images}
    log.info(f"Testing - search {number_images} images with provided API key")
    response = client_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == number_images

@pytest.mark.parametrize("number_images", [101, 105, 203])
def test_search_up_to_100_images_key(client_key, number_images) -> None:
    """ Test that searching more than 100 images with API key returns 100 images """
    payload = {"limit": number_images}
    log.info(f"Testing - search {number_images} images with provided API key")
    response = client_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 100

@pytest.mark.parametrize("number_images", [15])
def test_search_images_with_breed(client_key, number_images) -> None:
    """ Test that searching it is possible to search for images with breed info """
    payload = {"has_breeds": True, "limit": number_images}
    log.info(f"Testing - search images with provided API key and breed info")
    response = client_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == number_images
    for image in response_data:
        assert image.get("breeds")

def test_search_images_pagination(client_key) -> None:
    payload = {"page": 2, "limit": 100}
    log.info(f"Testing - search images with provided API key and pagination")
    response = client_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 100
    assert all(
        header_item in response.headers for header_item in ["Pagination-Count", "Pagination-Page", "Pagination-Limit"]
    )
    assert response.headers.get("Pagination-Page") == "2"
