#special file used by pytest to deffine shared fixtures that can be used across multiple test files without importing them manually
import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def sample_book():
    return{"title" : "the alchemist","author":"Paulo coelho"}

@pytest.fixture
def add_sample_books(sample_book):#sends req to add book
    response = requests.post(f"{BASE_URL}/books", json= sample_book)#send post req to books with sample_book as json
    assert response.status_code == 201
    return response.json() #Converts the API's JSON response to a Python dictionary.



@pytest.fixture
def updated_book():
    return{"title" : "5am club", "author":"robin sharma"}
@pytest.fixture
def update_title_only():
    return{"title":"5am club"}




@pytest.fixture(autouse=True)#autouse=True ensures this runs before every test without needing to mention it explicitly.
def reset_books():
    """Reset the book list before each test automatically."""
    requests.post(f"{BASE_URL}/reset")

#parameterization with fixtures

@pytest.fixture(params=[
    {"title": "1984", "author": "George Orwell"},
    {"title": "Brave New World", "author": "Aldous Huxley"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury"}
])

def book_data(request):
    return request.param

@pytest.fixture
def create_book(book_data):
    response = requests.post(f"{BASE_URL}/books",json = book_data)
    assert response.status_code == 201
    return response.json(), book_data
