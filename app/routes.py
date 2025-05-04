from flask import Flask, jsonify,request

app = Flask(__name__) #create a flask app object, name helps flask to locate app
books = []  #temp list, using instead of db

@app.route('/books',methods =['GET']) #route decorator,It tells Flask:When someone goes to /books with a GET request, run the function below
def get_books():
    return jsonify(books), 200 # convert list to json

@app.route('/books',methods=['POST'])#runs while someone send new data to books
def add_books():
    data = request.get_json()
    if not data.get('title') or not data.get('author'):
        return jsonify({"error": "Missing data"}) , 400
    book = {"id": len(books) + 1, "title":data['title'], "author":data['author'] }  #create a dictionary

    books.append(book) #add new book to list
    return jsonify(book), 201 #created


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data=request.get_json()
    for book in books:
        if book["id"] == book_id:
            book["title"] = data.get("title", book["title"])
            book["author"] = data.get("author", book["author"])
            return jsonify(book), 200
    return jsonify({"error": "book not found"}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books #If you modify the books list itself — like replacing it or reassigning it — you need to declare it global. But if you're just modifying its contents (like changing an item inside), you do not need global.
    for book in books:
        if book["id"] == book_id:
            books = [b for b in books if b["id"] != book_id] #remove targetted book from list
            return '',204
    return jsonify({"error": "book not found"}), 404


@app.route('/reset', methods=['POST'])  # Add this route
def reset_books():
    books.clear()
    return '', 204


@app.route('/')
def home():
    return "Welcome to the Bookstore API!"

