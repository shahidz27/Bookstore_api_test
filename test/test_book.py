import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

def test_add_book(add_sample_books,sample_book):
    assert add_sample_books["title"] == sample_book["title"]
    assert add_sample_books["author"] == sample_book["author"]
    assert "id" in add_sample_books and isinstance(add_sample_books["id"], int)#The response JSON contains a key named "id".The value of that "id" key is an integer

def test_get_book(add_sample_books):
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    books = response.json() #parse the json response to a list

    # Print the list of books to see the result
    print(f"Books in the response: {books}")
    assert isinstance(books,list) #expecting a list

    assert any(
        b["title"] == add_sample_books["title"] and b["author"] == add_sample_books["author"]
        for b in books
    ) #Checks all books in the list and will pass if any book matches the add_sample_book.


def test_update_book(add_sample_books,updated_book):
    book_id = add_sample_books["id"]
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=updated_book)
    assert response.status_code == 200

    updated = response.json()
    assert updated["id"] == book_id
    assert updated["title"] == updated_book["title"]
    assert updated["author"]  == updated_book["author"]

def test_update_only_title(add_sample_books):
    book_id = add_sample_books["id"]
    updated_data = {"title" : "only title changed"}
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=updated_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "only title changed"
    assert updated["author"] == add_sample_books["author"]

def test_update_nonexistent_book(updated_book):
    response = requests.put(f"{BASE_URL}/books/9999", json=updated_book)
    assert response.status_code == 404

def test_delete_book(add_sample_books):
    book_id = add_sample_books["id"]
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 204

    response_check = requests.get(f"{BASE_URL}/books")
    assert book_id not in [book["id"] for book in response_check.json()]

def test_delete_nonexistent_book():
    response = requests.delete(f"{BASE_URL}/books/9999")
    assert response.status_code == 404

#parameterisation

@pytest.mark.parametrize("book",[
    {"title": "1984", "author": "George Orwell"},
    {"title": "Brave New World", "author": "Aldous Huxley"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury"}])  # test_add_book() function 3 times, each with one of these dictionaries as book.
def test_paramadd_book(book):
    response = requests.post(f"{BASE_URL}/books",json = book)
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == book["title"]
    assert created["author"] == book["author"]
    assert "id" in created and isinstance(created["id"], int)

def test_add_withparam_fixture(create_book):
    created_book, original_data = create_book

    assert created_book["title"] == original_data["title"]
    assert created_book["author"] == original_data["author"]
    assert "id" in created_book and isinstance(created_book["id"], int)

