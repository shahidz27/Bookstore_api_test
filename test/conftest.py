# conftest.py
import pytest
from app.routes import app as flask_app

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_book():
    return {"title": "the alchemist", "author": "Paulo coelho"}

@pytest.fixture
def add_sample_books(client, sample_book):
    """Adds a sample book and returns the created book data."""
    response = client.post("/books", json=sample_book)
    assert response.status_code == 201
    return response.get_json()

@pytest.fixture
def updated_book():
    return {"title": "5am club", "author": "robin sharma"}

@pytest.fixture
def update_title_only():
    return {"title": "5am club"}

@pytest.fixture(autouse=True)
def reset_books(client):
    """Reset the book list before each test automatically."""
    client.post("/reset")

# Parameterization with fixtures
@pytest.fixture(params=[
    {"title": "1984", "author": "George Orwell"},
    {"title": "Brave New World", "author": "Aldous Huxley"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury"}
])
def book_data(request):
    return request.param

@pytest.fixture
def create_book(client, book_data):
    """Create a book using parameterized data."""
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    return response.get_json(), book_data