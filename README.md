# **IT CATS Test Suite**

This repository contains a test suite for verifying the functionality of [The Cat API](https://thecatapi.com). It includes tests for various endpoints such as searching, uploading, and deleting images, among others.

## **Table of Contents**

* Getting Started  
* Prerequisites  
* Installation  
* Running Tests  
* Reporting  
* Test Features  
* Project Structure

---

## **Getting Started**

Follow the instructions below to set up the project and run the test suite locally.

## **Prerequisites**

Make sure you have the following installed on your system:

* Python 3.8 or higher  
* pip (Python package manager)  
* The Cat API Key ([sign up for an account](https://thecatapi.com/#pricing) to get your API key)

## **Installation**

Clone the repository:  
**git clone https://github.com/yourusername/cat-api-test-suite.git**  
**cd cat-api-test-suite**

Create and activate a virtual environment (Unix-based):  
**python \-m venv .venv**  
**source .venv/bin/activate**

Create and activate a virtual environment (Windows):  
**python \-m venv .venv**  
**.venv\\Scripts\\activate**  
Install the required dependencies:  
**pip install \-r requirements.txt**

Set up the **.env** file in the root directory (rename **.env.example** file) with the following keys:  
**CAT\_URL=\<https://api.thecatapi.com/v1\>**  
**CAT\_API\_KEY=\<your\_api\_key\_here\>**

## **Running Tests**

To run the tests, use the following commands (current working directory is it\_cats):

    pytest
        # to run all tests
    pytest test\_cats/tests/test\_cat\_api
        #  to run all tests under the "test\_cat\_api" directory
    pytest test\_cats/tests/test\_cat\_api/test\_base.py
        # to run all tests from the "test\_base.py" test file 
    # or simply run specific test with your IDE (click on the test name and select Run option

## **Reporting**

To generate HTML test report and output.json files run the following command:

    pytest tests/ --html-report=./report --title='Your Title’ 
        # customize the report location, filename and title

## **Test Features**

This test suite covers the following functionality of The Cat API:

1. **Base API Validation:**  
   * Open The Cat API with API key and without  
2. **Image Search**:  
   * Fetch images by parameters with API key and without  
   * Validate image metadata  
3. **Image Upload**:  
   * Upload image file  
   * Validate successful upload  
4. **Image Delete**:  
   * Delete uploaded image  
   * Confirm the appropriate error message for not account file deletion  
5. **Breeds Search:**  
   * Fetch breeds with API key  
6. **General API Validation**:  
   * Test responses with and without API keys  
   * Check status codes, headers, and response body structures

## **Project Structure**

**it\_cats/**  
**├── test\_cats/**  
**│   ├── tests/**  
**│   │   ├── test\_cat\_api/**  
**│   │   │   ├── test\_base.py**                   
**│   │   │   ├── test\_breeds.py**                 
**│   │   │   ├── test\_images\_delete.py**          
**│   │   │   ├── test\_images\_search\_key.py**      
**│   │   │   ├── test\_images\_search\_no\_key.py**   
**│   │   │   ├── test\_images\_upload.py**          
**│   │   ├── test\_data/**  
**│   │       ├── cat\_sample.json**  
**│   │       ├── kitty.jpg**  
**│   ├── conftest.py**  
**├── test\_report/**  
**│   ├── output.json**  
**│   ├── pytest\_html\_report.html**  
**├── .env.example**  
**├── .gitignore**  
**├── pytest.ini**  
**├── README.md**  
**├── requirements.txt**  