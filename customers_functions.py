from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import Customers
def customers_register_routes(app, db):
    # shows all customers
    @app.route('/customers')
    def show_customer():
        customers=Customers.query.all()
        customers_data=[]
        for customer in customers:
                customers_data.append({
                    'id': customer.id, 
                    'name': customer.name,
                    'age': customer.age,
                    'email': customer.email,
                    'phone_number': customer.phone_number,
                    'city': customer.city
                })
        return jsonify(customers_data), 200
    # add new customers to Customers table
    @app.route('/add_customers', methods=['POST'])
    def add_customers():
        data = request.json
        try:
            new_customer = Customers(
                name=data['name'],
                age=data['age'],
                email=data['email'],
                phone_number=data['phone_number'],
                city=data['city'])
            db.session.add(new_customer)
            db.session.commit()
            app.logger.info(f"Customer {data['name']} added successfully.")
            return jsonify({"message": "Customer was added successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding customer {data['name']}: {str(e)}")
            return jsonify({"error": "Customer already exists!"}),500
    # delete customer from table by id
    @app.route('/del_customers/<int:id>',methods=['DELETE'])
    @jwt_required()  
    def delete_customers(id):
        item=Customers.query.get(id)
        try:
            if item:
                db.session.delete(item)
                db.session.commit()
                app.logger.info(f"Customer {item} was deleted successfully.")
                return jsonify({'message': 'Customer has been deleted successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting customer {item}: {str(e)}")
            return jsonify({"error": "Customer not found or has a loan in his name!"}),500

    # update customer info in table by id
    @app.route('/edit_customers/<int:id>', methods=['PUT'])
    @jwt_required()  
    def update_customer(id):
        data = request.json
        customer = Customers.query.get(id)
        if not customer:
            app.logger.error(f"Customer {id} not found")
            return jsonify({"message": "Customer ID not found!"})
        # Update customer fields only if new data is provided
        if 'name' in data and data['name']:
            customer.name = data['name'] 
        if 'age' in data and data['age']:
            customer.age = data['age']
        if 'email' in data and data['email']:
            customer.email = data['email']
        if 'phone_number' in data and data['phone_number']:
            customer.phone_number = data['phone_number']
        if 'city' in data and data['city']:
            customer.city = data['city']
        try:
            db.session.commit()
            app.logger.info(f"Customer {customer.name} info has been updated successfully.")
            return jsonify({'message': 'Customer info has been updated successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating customer {customer.name}: {str(e)}")
            return jsonify({"message": "Customer ID not found!"}), 404
    # search customer by name
    @app.route('/search_customer/<string:name>')
    @jwt_required()  
    def search_customers(name):
        customers = Customers.query.filter(Customers.name.ilike(f"%{name}%")).all()
        try:
            searched_customer= [{
                'name': customer.name,
                'email': customer.email,
                'phone_number': customer.phone_number,
                'age': customer.age,
                'city': customer.city,
            } for customer in customers]
            app.logger.info(f"{name} was found successfully.")
            return jsonify(searched_customer)
        except Exception as e:
            app.logger.error(f"Error searching for customer {name}: {str(e)}")
            return jsonify({"error": str(e)}), 500
            
