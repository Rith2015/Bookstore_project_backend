from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import Loans, Customers, Books,Loan_time

def loans_register_routes(app, db):
    @app.route('/loan_book', methods=['POST'])
    def loan_books():
        data = request.json
        # Check if the customer ID exists
        customer = Customers.query.filter_by(name=data['customer_name']).first()
        if not customer:
            return jsonify({"error": "Invalid customer name"}), 400
        # Check if the book exists by its name
        book = Books.query.filter_by(name=data['book_name']).first()
        if not book:
            return jsonify({"error": "Invalid book name"}), 400
        # Check if the book is available
        if book.status != "Available":
            return jsonify({"error": "This book is currently unavailable"}), 400
        try:
            loan_date_str = data.get('loanDate')   # Extract the loan date from the request
            loan_date = datetime.strptime(loan_date_str, '%d/%m/%Y')  # Adjust to the correct format

            # Retrieve the loan time type for the book
            loan_time = Loan_time.query.get(book.loan_time_type_id) 
            if not loan_time:
                return jsonify({"error": "Loan time type not found for the book."}), 400
            
            loan_duration = int(loan_time.total_days)  # Convert to integer
            
            # Calculate return date based on the loan duration
            return_date = loan_date + timedelta(days=loan_duration)  # Add the duration to loan date
            
            new_loan = Loans(
                customer_id=customer.id,
                book_id=book.id,
                loanDate=loan_date_str,
                returnDate = return_date.strftime('%d/%m/%Y'),  # Store return date in d/m/y format
                status="Active"
            )
            db.session.add(new_loan)
            book.status = "Unavailable"
            db.session.commit()
            app.logger.info({f"Loan was successfully added and {book.name} is now unavailable."})
            return jsonify({"message": f"Loan was successfully added and {book.name} is now unavailable!"}), 201 
        except ValueError as e:
            return jsonify({"error": "Invalid date format: " + str(e)}), 400
        except Exception as e:
            db.session.rollback()
            app.logger.error({{"error": str(e)}})
            return jsonify({"error": str(e)}), 500
    # shows all loans
    @app.route('/show_loans')
    def show_loans():
        all_loans=Loans.query.all()
        loans=[]
        for loan in all_loans:
            loans.append({
            'id':loan.id,
            'customer_id':loan.customer_id,
            'book_id':loan.book_id,
            'loanDate':loan.loanDate,
            'returnDate':loan.returnDate,
            'status':loan.status
            })
        return jsonify(loans), 200
    # shows all loan with status Late in them
    @app.route('/show_late_loans')
    def show_late_loans():
        all_loans=Loans.query.filter_by(status='Late').all()
        loans=[]
        for loan in all_loans:
            loans.append({
            'id':loan.id,
            'customer_id':loan.customer_id,
            'book_id':loan.book_id,
            'loanDate':loan.loanDate,
            'returnDate':loan.returnDate,
            'status':loan.status
            })
        return jsonify(loans), 200
    
    # delete loans columns
    @app.route('/return_book', methods=['DELETE'])
    def return_books():
        customer_name = request.args.get('customer_name')
        book_name = request.args.get('book_name')
        # Check if the customer ID exists
        customer = Customers.query.filter_by(name=customer_name).first()
        if not customer:
            return jsonify({"error": "Invalid customer name"}), 400
        # Check if the book exists by its name
        book = Books.query.filter_by(name=book_name).first()
        if not book:
            return jsonify({"error": "Invalid book name"}), 400
        # Check if the book is available
        if book.status != "Unavailable":
            return jsonify({"error": "This loan not found or book already been returned."}), 400
        try:
            # Find the existing loan where the book is currently loaned by the customer
            existing_loan = Loans.query.filter_by(customer_id=customer.id, book_id=book.id).first()
            if not existing_loan:
                return jsonify({"error": "No loan found for both this book and customer."}), 400
            db.session.delete(existing_loan)
            # Mark the book as available
            book.status = "Available"
            db.session.commit()
            app.logger.info({f"Loan was successfully returned, and {book.name} is now available!"})
            return jsonify({"message": f"Loan was successfully returned, and {book.name} is now available!"}), 200
        except Exception as e:
            db.session.rollback()
            app.logger.error({{"error": str(e)}})
            return jsonify({"error": str(e)}), 500
    # deletes loan by id
    @app.route('/del_loan/<int:id>',methods=['DELETE'])
    def del_loan(id):
        try:
            # Get the loan by ID
            existing_loan = Loans.query.get(id)
            if not existing_loan:
                return jsonify({"error": "No loan found with this ID."}), 400
            
            # Fetch the book associated with the loan
            book = Books.query.get(existing_loan.book_id)
            if not book:
                return jsonify({"error": "Book not found!"}), 404
            # Mark the book as available
            book.status = "Available"
            # Delete the loan record
            db.session.delete(existing_loan)
            db.session.commit()
            app.logger.info({f"Loan was deleted successfully, and '{book.name}' is now available!"})
            return jsonify({"message": f"Loan was deleted successfully, and '{book.name}' is now available!"}), 200
        except Exception as e:
            db.session.rollback()
            app.logger.error({{"error": str(e)}})
            return jsonify({"error": str(e)}), 500
     # update loan info in table by id
    @app.route('/edit_loans/<int:id>', methods=['PUT'])
    def update_loans(id):
        data = request.json
        loan = Loans.query.get(id)
        if not loan:
            app.logger.error(f"Loan {id} not found")
            return jsonify({"message": "Loan ID not found!"})
        # Update loan fields only if new data is provided
        if 'customer_id' in data and data['customer_id']:
            loan.customer_id = data['customer_id'] 
        if 'book_id' in data and data['book_id']:
            loan.book_id = data['book_id']
        if 'loanDate' in data and data['loanDate']:
            loan.loanDate = data['loanDate']
        if 'returnDate' in data and data['returnDate']:
            loan.returnDate = data['returnDate']
        try:
            db.session.commit()
            app.logger.info(f"loan {loan.id} info has been updated successfully.")
            return jsonify({'message': 'loan info has been updated successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating loan {loan.id}: {str(e)}")
            return jsonify({"message": "loan ID not found!"}), 404 
    # shows loan time types info
    @app.route('/loan_time')
    def show_loan_time():
        loan_times=Loan_time.query.all()
        time_data=[]
        for loan in loan_times:
            time_data.append({
                'id':loan.id,
                'duration':loan.duration,
                'total_days':loan.total_days
            })
        return jsonify(time_data), 200
    
    # makes book be Unavailable
    @app.route('/loan_status_late/<int:id>',methods=['Put'])
    def late_loan(id):
        item=Loans.query.get(id)
        if item:
            item.status="Late"
            db.session.commit()
            return jsonify({'message': f'Book {item.name} has been marked as unavailable!'}), 200
        else:
            return jsonify({"message": "Book id not found!"}), 404
        
    # Make_books_available
    @app.route('/loan_status_active/<int:id>',methods=['Put'])
    def loan_status(id):
        item=Loans.query.get(id)
        if item:
            item.status="Active"
            db.session.commit()
            return jsonify({'message': f'Book {item.name} has been marked as available!'}), 200
        else:
            return jsonify({"message": "Book id not found!"}), 404 