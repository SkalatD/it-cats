import pytest
import requests
import os
import logging
import json
import base64
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any


log = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
# Define global constants (set environment variables as values)
current_dir = Path(__file__).parent
it_cats_root = current_dir.parents[0]
env_path = it_cats_root / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    log.warning(
        f".env file not found at {env_path}. Please ensure it exists. "
        "Only requests that do not require authentication will proceed!"
    )

BASE_URL = os.getenv(key="CAT_URL", default="https://api.thecatapi.com/v1")
API_KEY = os.getenv(key="CAT_API_KEY")

# ----------------------------------------------------------------------------------------------------------------------
@pytest.fixture()
def api_client():
    """ Pytest fixture to provide reusable API client for tests.

    Provides logic for making HTTP requests to a specified API,
    initializes API client with a base URL and optionally an API key. The API key can be set to 'None' for requests
    that do not require authentication.

    :returns: an instance of the APIClient class, configured with a base URL and API key

    """
    class APIClient:
        """ API client for sending HTTP requests to a specific API.

        :param base_url: the base URL of the API
        :param headers: a dictionary of custom headers to include in requests
        :param api_key: the API key used for authorization, if required

        """
        def __init__(self, base_url: str, headers: Optional[Dict[str, str]], api_key: bool = False) -> None:
            self.base_url = base_url
            self.headers = headers if headers else {}
            self.api_key = api_key

        def get(self, endpoint: Optional[str]=None, params: Optional[Dict[str, Any]]=None) -> requests.Response:
            """ Sends a GET request to the specified API endpoint.

            :param endpoint: the API endpoint (relative to the base URL), if not provided - base URL is used
            :param params: query parameters for the GET request

            :returns: the HTTP response object

            """
            # Use base URL global value if endpoint value is not provided
            url = f"{self.base_url}{endpoint}" if endpoint else f"{self.base_url}"
            log.info(f"Testing endpoint url: {url}")
            return requests.get(url=url, headers=self.headers, params=params)

        def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
        ) -> requests.Response:
            """ Sends a POST request to the specified API endpoint.

            :param endpoint: the API endpoint (relative to the base URL)
            :param data: data to send with the POST request
            :param json: JSON payload to send with the POST request

            :returns: the HTTP response object

            """
            url = f"{self.base_url}{endpoint}"
            log.info(f"Testing endpoint url: {url}")
            return requests.post(url, headers=self.headers, data=data, json=json)

        def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
            """ Sends a DELETE request to the specified API endpoint.

            :param endpoint: the API endpoint (relative to the base URL)
            :param params: query parameters for the DELETE request

            :returns: the HTTP response object

            """
            url = f"{self.base_url}{endpoint}"
            log.info(f"Testing endpoint url: {url}")
            return requests.delete(url, headers=self.headers, params=params)

    def _create_client(headers: Optional[Dict[str, str]] = None, api_key: bool = False) -> APIClient:
        """ Creates an APIClient instance with an optional API key.

        :param headers: dictionary of headers
        :param api_key: the API key for authentication, defaults to the global API_KEY

        :returns: an instance of the APIClient class

        """
        if not headers:
            headers = {}

        if api_key:
            if API_KEY:
                # Add authorization header if the API key is provided
                headers["x-api-key"] = API_KEY
                log.info("CAT_API_KEY environment variable found")
            else:
                log.warning("CAT_API_KEY environment variable is not set. Please set it in .env file!")

        return APIClient(base_url=BASE_URL, headers=headers, api_key=api_key)

    return _create_client

@pytest.fixture(scope="module")
def load_test_data():
    """ Fixture to load test data from a JSON file.

    :returns: A function that takes a JSON file name as input and returns the parsed JSON data

    """
    test_data_dir = it_cats_root / f"test_cats/tests/test_data/"
    def get_file(file_name: str) -> Any:
        """ Loads and parses JSON data from a file in the test data directory.

        :param file_name: The name of the JSON file (without extension) to load

        :returns: The JSON data parsed into a Python object
        :raises FileNotFoundError: If the file does not exist
        :raises json.JSONDecodeError: If the file contents are not valid JSON

        """
        if not file_name:
            raise ValueError("File name must be provided!")

        # Ensure file name does not have an extension
        file_name = file_name.replace(".json", "")
        # Construct the file path
        test_data_file = test_data_dir / f"{file_name}.json"

        # Read and return JSON content
        with open(test_data_file, mode="r") as file:
            return json.load(file)

    return get_file

@pytest.fixture(scope="module")
def get_test_image():
    """ Fixture to get test image path.

    :returns: test image

    """
    test_data_dir = it_cats_root / f"test_cats/tests/test_data/"
    def get_image(image_file: str) -> str:
        """ Gets image binary string from the specified image file in the test data directory.

        :param image_file: The name of the image file (with extension) to load

        :returns: binary content from image file as a string
        :raises FileNotFoundError: if the image does not exist
        :raises IOError: if there is an issue opening or reading the file

        """
        if not image_file:
            raise ValueError("Image name must be provided!")

        test_image_path = test_data_dir / f"{image_file}"
        with open(file=test_image_path, mode="rb") as image:
            image_data = image.read()
            image_content = base64.b64encode(image_data).decode("utf-8")

        return image_content

    return get_image
