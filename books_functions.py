from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import Books, Loan_time
def books_register_routes(app, db):      
    # functions and Routes

    # shows all books info
    @app.route('/books')
    def show_books():
        books = Books.query.all()
        loan_times = Loan_time.query.all()  # Assuming this returns a list of Loan_time objects
        loan_data = {ltem.id: ltem.duration for ltem in loan_times}  # Create a dictionary for quick access
        books_data = []
        for book in books:
            books_data.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'category': book.category,
                'year_published': book.year_published,
                'duration': loan_data.get(book.loan_time_type_id),
                'status': book.status,
                'image_url': book.image_url
            })
        
        return jsonify(books_data), 200
    
    # add new books to Book table
    @app.route('/add_books', methods=['POST'])
    @jwt_required()  
    def add_book():
        data = request.json
        loan_time_type_id = data.get('loan_time_type_id')
        if not Loan_time.query.get(loan_time_type_id):
            return jsonify({"error": "Invalid loan time ID"}), 400
        try:
            new_book = Books(
                name=data['name'],
                author=data['author'],
                category=data['category'],
                year_published=data['year_published'],
                loan_time_type_id=loan_time_type_id,
                status='Available',
                image_url= data['image_url'])
            
            db.session.add(new_book)
            db.session.commit()
            app.logger.info(f"{data['name']} added successfully.")
            return jsonify({"message": "Book was added successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding customer {data['name']}: {str(e)}")
            return jsonify({"error": f"Book was not added! Error: {str(e)}"}), 500
    # makes book be Unavailable
    @app.route('/Make_books_Unavailable/<int:id>',methods=['Put'])
    def Unavailable_books(id):
        item=Books.query.get(id)
        if item:
            item.status="Unavailable"
            db.session.commit()
            return jsonify({'message': f'Book {item.name} has been marked as unavailable!'}), 200
        else:
            return jsonify({"message": "Book id not found!"}), 404
        
    # Make_books_available
    @app.route('/make_books_available/<int:id>',methods=['Put'])
    def available_books(id):
        item=Books.query.get(id)
        if item:
            item.status="Available"
            db.session.commit()
            return jsonify({'message': f'Book {item.name} has been marked as available!'}), 200
        else:
            return jsonify({"message": "Book id not found!"}), 404 

   # Update book info in table by id
    @app.route('/edit_books/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_book(id):
        data = request.json
        item = Books.query.get(id)
        if not item:
            app.logger.error(f"Book {id} not found")
            return jsonify({"message": "Book ID not found!"}), 400
        
        loan_time_type_id = data.get('loan_time_type_id')
        if loan_time_type_id and not Loan_time.query.get(loan_time_type_id):
            return jsonify({"message": "Invalid loan time type ID!"}), 400

        # Update only fields that have new info in them
        if 'name' in data and data['name']:
            item.name = data['name']
        if 'author' in data and data['author']:
            item.author = data['author']
        if 'category' in data and data['category']:
            item.category = data['category']
        if 'year_published' in data and data['year_published']:
            item.year_published = data['year_published']
        if loan_time_type_id:
            item.loan_time_type_id = loan_time_type_id
        try:
            db.session.commit()
            app.logger.info(f"{item.name} has been updated successfully.")
            return jsonify({'message': 'Book info has been updated successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error update {item.name} info")
            return jsonify({"error": f"Failed to update book: {str(e)}"}), 500
    # search for book by name
    @app.route('/search_books/<name>')
    def search_books(name):
        books = Books.query.filter(Books.name.ilike(f"%{name}%")).all()
        loan_times = Loan_time.query.all() 
        loan_data = {ltem.id: ltem.duration for ltem in loan_times}
        try:
            searched_book=[{
            'name': book.name,
            'author': book.author,
            'image_url': book.image_url,
            'category': book.category,
            'year_published':book.year_published,
            'status': book.status,
            'duration': loan_data.get(book.loan_time_type_id),  
            }for book in books]
            app.logger.info(f"{name} was found successfully.")
            return jsonify(searched_book)
        except Exception as e:
            app.logger.error(f"Error searching for {name}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    # search book by author
    @app.route('/search_author/<author>')
    def search_author(author):
        books = Books.query.filter(Books.author.ilike(f"%{author}%")).all()
        loan_times = Loan_time.query.all() 
        loan_data = {ltem.id: ltem.duration for ltem in loan_times}
        try:
            searched_book=[{
            'name': book.name,
            'author': book.author,
            'image_url': book.image_url,
            'category': book.category,
            'year_published':book.year_published,
            'status': book.status,
            'duration': loan_data.get(book.loan_time_type_id),  
            }for book in books]
            app.logger.info(f"{author} was found successfully.")
            return jsonify(searched_book)
        except Exception as e:
            app.logger.error(f"Error searching for {author}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    # deletes book from table
    @app.route('/del_book/<int:id>',methods=['DELETE'])
    def del_books(id):
        item=Books.query.get(id)
        try:
            if item:
                db.session.delete(item)
                db.session.commit()
                app.logger.info(f"Book {item} was deleted successfully.")
                return jsonify({'message': 'Book has been deleted successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting book {item}: {str(e)}")
            return jsonify({"error": "Book not found!"}),500


