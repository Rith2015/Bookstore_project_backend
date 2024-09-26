from logging.handlers import RotatingFileHandler
import os
import subprocess
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from books_functions import books_register_routes
from customers_functions import customers_register_routes
from loans_functions import loans_register_routes
from admin_functions import admin_register_routes
from models import db
import logging
from seed_table_data import seed_data

app = Flask(__name__)
CORS(app)
app.secret_key = 'secret_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)  # Adjust this level to what you need
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

books_register_routes(app, db)
customers_register_routes(app,db)
loans_register_routes(app,db)
admin_register_routes(app,db)

@app.route('/reset_table')
def table_delete():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Seed the tables with default data
        seed_data()


if __name__=="__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)