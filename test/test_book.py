import pytest


def test_add_book(add_sample_books, sample_book):
    assert add_sample_books["title"] == sample_book["title"]
    assert add_sample_books["author"] == sample_book["author"]
    assert "id" in add_sample_books and isinstance(add_sample_books["id"], int)


def test_get_book(client, add_sample_books):
    response = client.get("/books")
    assert response.status_code == 200
    books = response.get_json()

    print(f"Books in the response: {books}")
    assert isinstance(books, list)

    assert any(
        b["title"] == add_sample_books["title"] and b["author"] == add_sample_books["author"]
        for b in books
    )


def test_update_book(client, add_sample_books, updated_book):
    book_id = add_sample_books["id"]
    response = client.put(f"/books/{book_id}", json=updated_book)
    assert response.status_code == 200

    updated = response.get_json()
    assert updated["id"] == book_id
    assert updated["title"] == updated_book["title"]
    assert updated["author"] == updated_book["author"]


def test_update_only_title(client, add_sample_books):
    book_id = add_sample_books["id"]
    updated_data = {"title": "only title changed"}
    response = client.put(f"/books/{book_id}", json=updated_data)
    assert response.status_code == 200

    updated = response.get_json()
    assert updated["title"] == "only title changed"
    assert updated["author"] == add_sample_books["author"]


def test_update_nonexistent_book(client, updated_book):
    response = client.put("/books/9999", json=updated_book)
    assert response.status_code == 404


def test_delete_book(client, add_sample_books):
    book_id = add_sample_books["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    response_check = client.get("/books")
    assert book_id not in [book["id"] for book in response_check.get_json()]


def test_delete_nonexistent_book(client):
    response = client.delete("/books/9999")
    assert response.status_code == 404


@pytest.mark.parametrize("book", [
    {"title": "1984", "author": "George Orwell"},
    {"title": "Brave New World", "author": "Aldous Huxley"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury"}
])
def test_paramadd_book(client, book):
    response = client.post("/books", json=book)
    assert response.status_code == 201
    created = response.get_json()
    assert created["title"] == book["title"]
    assert created["author"] == book["author"]
    assert "id" in created and isinstance(created["id"], int)


def test_add_withparam_fixture(create_book):
    created_book, original_data = create_book
    assert created_book["title"] == original_data["title"]
    assert created_book["author"] == original_data["author"]
    assert "id" in created_book and isinstance(created_book["id"], int)