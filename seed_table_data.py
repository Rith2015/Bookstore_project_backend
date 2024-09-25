from flask_bcrypt import Bcrypt
import bcrypt
bcrypt = Bcrypt()
from models import Loan_time,Loans,Books,Customers,Admin_users,db

# when table is empty or has been deleted, this functions add defult info into the empty tables
def seed_data():
    if not Loan_time.query.first():  # Check if Loan_time table is empty
        loan_times = [
            Loan_time(duration='Up to 10 days',total_days=10),
            Loan_time(duration='Up to 5 days',total_days=5),
            Loan_time(duration='Up to 2 days',total_days=2)
        ]
        db.session.bulk_save_objects(loan_times)

    if not Books.query.first():  # Check if Books table is empty
        books = [
            Books(name='The Shining', author='Stephen King', category='Horror', year_published='1977', loan_time_type_id=1,status='Available', image_url="https://cdn.waterstones.com/bookjackets/large/9781/4447/9781444720723.jpg"),
            Books(name='Dracula', author='Bram Stoker', category='Gothic Horror', year_published='1897', loan_time_type_id=2, status='Unavailable', image_url="https://cdn.waterstones.com/bookjackets/large/9781/4351/9781435159570.jpg"),
            Books(name='To Kill a Mockingbird', author='Harper Lee', category='Southern Gothic', year_published='1960', loan_time_type_id=1, status='Available', image_url="https://cdn.waterstones.com/bookjackets/large/9780/0995/9780099549482.jpg"),
            Books(name='Moby Dick', author='Herman Melville', category='Adventure', year_published='1851', loan_time_type_id=3, status='Unavailable', image_url="https://cdn.waterstones.com/bookjackets/large/9780/1424/9780142437247.jpg"),
            Books(name='The Great Gatsby', author='F. Scott Fitzgerald', category='Classic Fiction', year_published='1925', loan_time_type_id=1, status='Unavailable', image_url="https://cdn.waterstones.com/bookjackets/large/9780/1411/9780141182636.jpg"),
            Books(name='Pride and Prejudice', author='Jane Austen', category='Romance', year_published='1813', loan_time_type_id=2, status='Available', image_url="https://cdn.waterstones.com/bookjackets/large/9780/1414/9780141439518.jpg"),
            Books(name='1984', author='George Orwell', category='Dystopian Fiction', year_published='1949', loan_time_type_id=2, status='Unavailable', image_url="https://cdn.waterstones.com/bookjackets/large/9780/1411/9780141187761.jpg"),
            Books(name='The Catcher in the Rye', author='J.D. Salinger', category='Classic Fiction', year_published='1951', loan_time_type_id=1, status='Unavailable', image_url="https://cdn.waterstones.com/bookjackets/large/9780/2419/9780241984758.jpg"),
            Books(name='It', author='Stephen King', category='Horror', year_published='1986', loan_time_type_id=1, status='Unavailable', image_url="https://cdn.waterstones.com/bookjackets/large/9781/4447/9781444707861.jpg"),
            Books(name='Carrie', author='Stephen King', category='Horror', year_published='1974', loan_time_type_id=3, status='Available', image_url="https://cdn.waterstones.com/bookjackets/large/9781/4447/9781444720693.jpg"),
            Books(name='Percy Jackson & The Olympians: The Lightning Thief', author='Rick Riordan', category='Fantasy', year_published='2005', loan_time_type_id=1, status='Available', image_url="https://cdn.waterstones.com/bookjackets/large/9780/1413/9780141346809.jpg"),
            Books(name='Harry Potter and the Philosopher Stone', author='J.K. Rowling', category='Fantasy', year_published='1997', loan_time_type_id=1, status='Available', image_url="https://cdn.waterstones.com/bookjackets/large/9781/4088/9781408855652.jpg"),


        ]
        db.session.bulk_save_objects(books)
    if not Customers.query.first():# Check if Customers table is empty
        customers=[
            Customers(name='John Doe', email='john.doe@example.com', phone_number='555-1234', age=35, city='New York'),
            Customers(name='Jane Smith', email='jane.smith@example.com', phone_number='555-5678', age=28, city='Los Angeles'),
            Customers(name='Michael Johnson', email='michael.j@example.com', phone_number='555-8765', age=42, city='Chicago'),
            Customers(name='Emily Davis', email='emily.d@example.com', phone_number='555-4321', age=30, city='Houston'),
            Customers(name='Robert Wilson', email='robert.w@example.com', phone_number='555-2345', age=50, city='Miami'),
            Customers(name='Wade Wilson', email='wade.wilson@chimichangas.com', phone_number='555-1991', age=30, city='Philadelphia'),
            Customers(name='James Brown', email='james.b@example.com', phone_number='555-9876', age=38, city='Philadelphia'),
            Customers(name='Laura Martinez', email='laura.m@example.com', phone_number='555-6789', age=25, city='Chicago')
        ]
        db.session.bulk_save_objects(customers)
    if not Loans.query.first():# Check if Loans table is empty
        loans=[
            Loans(customer_id=1, book_id=2,loanDate="01/08/2024",returnDate="06/08/2024",status='Active'),
            Loans(customer_id=3, book_id=4,loanDate="06/09/2024",returnDate="9/09/2024",status='Late'),
            Loans(customer_id=5, book_id=5,loanDate="02/09/2024",returnDate="13/09/2024",status='Active'),
            Loans(customer_id=1, book_id=9,loanDate="01/09/2024",returnDate="11/09/2024",status='Late'),
            Loans(customer_id=8, book_id=8,loanDate="01/08/2024",returnDate="11/08/2024",status='Late')
            
        ]
        db.session.bulk_save_objects(loans)
    
    if not Admin_users.query.first():# Check if Admin users table is empty
        username='Admin'
        password='admin123'
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Admin_users(username=username, password=hashed_password)
        db.session.add(new_user)
    db.session.commit()