from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(130), nullable=False)
    year_published = db.Column(db.String(120), nullable=False)
    loan_time_type_id = db.Column(db.ForeignKey('loan_time.id'), nullable=False)
    loanTime = db.relationship('Loan_time', backref=db.backref('books', lazy=True))
    status = db.Column(db.String(80), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), unique=True, nullable=False)
    age=db.Column(db.String(180), nullable=False)
    email=db.Column(db.String(200), unique=True, nullable=False)
    phone_number=db.Column(db.String(20), unique=True, nullable=False)
    city=db.Column(db.String(180), nullable=False)

class Loan_time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.String(180), nullable=False)
    total_days=db.Column(db.String(180), nullable=False)

class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id=db.Column(db.ForeignKey('customers.id'), nullable=False)
    customer=db.relationship('Customers', backref=db.backref('loans', lazy=True))
    book_id=db.Column(db.ForeignKey('books.id'), nullable=False, unique=True)
    book=db.relationship('Books', backref=db.backref('loans',lazy=True))
    loanDate=db.Column(db.String(180), nullable=False)
    returnDate=db.Column(db.String(180), nullable=False)
    status=db.Column(db.String(180), nullable=False)
    

class Admin_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)



