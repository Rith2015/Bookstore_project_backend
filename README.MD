# Flask Bookstore project backend
## Overview
This project is a Bookstore Management System developed using Flask and SQLAlchemy. It allows users to manage books, customers, loans, and admin users with functionalities such as adding, deleting, and viewing loans,books or customers. The system is designed to provide an efficient way to track book loans and their status.

## Features
- **Book Management**: Add, view, and manage books.
- **Customer Management**: Add and manage customer details.
- **Loan Management**: Loan books to customers and track their return status.
- **Admin Management**: Manage admin users, **default admin username: Admin, admin password: admin123**
- **Logging**: Integrated logging for monitoring application activities.
- **Seeding Data**: Initial data seeding for books, customers, loans, loan times, and admin users.

## Technologies Used
- Flask
- SQLAlchemy
- Flask-CORS
- Flask-Bcrypt
- SQLite
- Python

## Bookstore  Structure
- app.py -- Main application file
- seed_table_data.py -- Script for seeding initial data
- models.py -- Database models
- loans_functions.py -- Routes for loan management
- customers_functions.py -- Routes for customer management
- books_functions.py -- Routes for book management
- admin_functions.py -- Routes for admin management
- app.log -- Log file for application activities that is created after you run the application
- Bookstore.db -- SQLite database file, in the instance folder

## Installation
### 1. **Clone the repository**:
   git clone repository-url
### 2.**Install the required packages:**
pip install -r requirements.txt
## Run the application:
- python app.py
- Access the application at http://127.0.0.1:5000.
# Endpoints
## App Endpoints
- Delete /delete_tables: Deletes all tables in the database.
- POST/seed_data: Create all tables and Seed the tables with data from seed_table_data.
## Books Endpoints
- GET/books: Shows all books.
- POST/add_books: Add new books.
- PUT/Make_books_Unavailable: Turn book status into unavailable.
- PUT/make_books_available: Turn book status into available.
- PUT/edit_books: Edit books info by id.
- GET/search_books: Search books by book name.
- GET/search_author: Search books by author.
- DELETE/del_book: Deletes book from table.
## Customers Endpoints
- GET/customers: Shows all customers.
- POST/add_customers: Add new customers.
- PUT/edit_customers: Edit customers info by id.
- GET/search_customer: Search customers by book name.
- DELETE/del_customers: Deletes customer from table.
## Loan Endpoints
- POST /loan_book: Loan a book to a customer.
- GET /show_loans: Show all loans.
- GET /show_late_loans: Show loans with status 'Late'.
- DELETE /return_book: Return a loaned book.
- DELETE /del_loan: Delete a loan by ID.
- PUT/edit_loans: Edit loans info by id.
- GET/loan_time: Shows all loan time types info
- PUT/loan_status_late: Turn loan status into late.
- PUT/loan_status_active: Turn loan status into active.
## Admin Endpoints
- POST/login: Enter username and password to get access_token. **default admin username: Admin, admin password: admin123**
- POST/register: Creates new admin users.
### Data Seeding
The initial data for books, customers, loan times, and an admin user is seeded using the seed_table_data.py file. This data will be added when the application is first run if the tables is empty.

## Logging
Application activity is logged in app.log. This includes loan actions and errors. app.log is created after you run the application.
