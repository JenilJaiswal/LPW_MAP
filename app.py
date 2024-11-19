from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/"

mongo = PyMongo(app)

# Route to create a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if 'title' not in data or 'author' not in data or 'year' not in data:
        return jsonify({'message': 'Title, author, and year are required!'}), 400
    
    books_collection = mongo.db.books
    book = {
        'title': data['title'],
        'author': data['author'],
        'year': data['year']
    }
    result = books_collection.insert_one(book)
    return jsonify({
        'message': 'Book added successfully!',
        'id': str(result.inserted_id)
    }), 201

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books_collection = mongo.db.books
    books = books_collection.find()
    result = []
    for book in books:
        book['_id'] = str(book['_id'])  
        result.append(book)
    return jsonify(result), 200


@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    books_collection = mongo.db.books
    book = books_collection.find_one({'_id': ObjectId(id)})
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
    book['_id'] = str(book['_id'])
    return jsonify(book), 200


@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    books_collection = mongo.db.books
    book = books_collection.find_one({'_id': ObjectId(id)})
    
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404

    # Update the book with the new data
    books_collection.update_one({'_id': ObjectId(id)}, {
        '$set': {
            'title': data.get('title', book['title']),
            'author': data.get('author', book['author']),
            'year': data.get('year', book['year'])
        }
    })
    
    return jsonify({'message': 'Book updated successfully!'}), 200


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    books_collection = mongo.db.books
    result = books_collection.delete_one({'_id': ObjectId(id)})
    
    if result.deleted_count == 0:
        return jsonify({'message': 'Book not found!'}), 404
    
    return jsonify({'message': 'Book deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
