""" Test file to test The Cat API

NOTE: the api_client fixture is used in this file
Please, see the "conftest.py" file content in order to see the fixture details

To run the tests make sure that pytest is set as a default tests runner in your IDE

"""

import pytest
import logging
import re

log = logging.getLogger(__name__)
# Mandatory image keys
image_object_keys = ["id", "url", "width", "height"]
# Regex pattern for valid image/animation URLs
image_url_pattern = re.compile(
        pattern=r'^https://.*\.(jpg|jpeg|png|gif|bmp|webp|svg|tiff|tif|apng|ico)$',
        flags=re.IGNORECASE  # Case-insensitive for file extensions
    )

@pytest.fixture()
def client_no_key(api_client):
    log.info("Getting API client with no API key provided")
    yield api_client()

def test_search_random_image_no_key(client_no_key) -> None:
    """ Test that images/search endpoint returns image info """
    log.info("Testing - search random image with no provided API key")
    response = client_no_key.get(endpoint="/images/search")  # Testing images/search endpoint
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

@pytest.mark.known_issue
@pytest.mark.parametrize("number_images", [1, 2, 6, 10])
def test_search_up_to_10_images_no_key(client_no_key, number_images) -> None:
    """ Test that searching up to 10 images is successful with no API key """
    payload = {"limit": number_images}
    log.info(f"Testing - search {number_images} images with no provided API key")
    response = client_no_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == number_images


@pytest.mark.parametrize("number_images", [11, 52, 100, 101])
def test_search_more_than_10_images_no_key(client_no_key, number_images) -> None:
    """ Test that searching more than 10 images with no API key returns only 10 images """
    payload = {"limit": number_images}
    log.info(f"Testing - search {number_images} images with no provided API key")
    response = client_no_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 10

def test_search_images_with_allowed_payload(client_no_key) -> None:
    """ Test images searching with no API key and allowed payload """
    payload = {
        "size": "med",
        "mime_types": "png",
        "format": "json",
        "limit": 10
    }
    log.info(f"Testing - search 10 images with no provided API key and allowed payload")
    response = client_no_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 10
    assert isinstance(response_data, list)
    for image in response_data:
        assert all(image.get(key) >= 300 for key in image_object_keys[-2::])  # check width and height values
        assert str(image.get("url")).endswith(".png")
        assert isinstance(image, dict)

def test_search_images_with_src(client_no_key) -> None:
    """ Test images searching with no API key and allowed payload """
    payload = {"format": "src"}
    log.info(f"Testing - search image with src format and no provided API key")
    response = client_no_key.get(endpoint="/images/search", params=payload)  # Testing images/search endpoint
    assert response.status_code == 200
    assert isinstance(response.content, bytes)

def test_search_specific_image_by_id(client_no_key, load_test_data) -> None:
    """ Test image searching with no API key and specified image id """
    cat_id = load_test_data(file_name="cat_sample")["id"]
    log.info(f"Testing - search image by id ({cat_id}) and no provided API key")
    response = client_no_key.get(endpoint=f"/images/{cat_id}")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data.get("id") == cat_id
