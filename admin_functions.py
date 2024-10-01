import datetime 
from functools import wraps
import time
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import Admin_users
bcrypt = Bcrypt()

def admin_register_routes(app, db):
    bcrypt.init_app(app)  
    jwt = JWTManager(app)    
    # Generate a JWT
    def generate_token(user_id):
        expiration = int(time.time()) + 3600  # Set the expiration time to 1 hour from the current time
        payload = {'user_id': user_id, 'exp': expiration}
        token = jwt.encode(payload, 'secret-secret-key', algorithm='HS256')
        return token
    
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
            try:
                data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                current_user_id = data['user_id']
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401
            return f(current_user_id, *args, **kwargs)
        return decorated

    def model_to_dict(model):
        serialized_model = {}
        for key in model.__mapper__.c.keys():
            serialized_model[key] = getattr(model, key)
        return serialized_model
    # login with a admin user to get access token
    @app.route('/login', methods=['POST'])
    def login():
        data =request.get_json()
        username = data["username"]
        password = data["password"]
        # Check if the user exists
        user = Admin_users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Generate an access token with an expiration time
            expires = datetime.timedelta(hours=1)
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            print(access_token)
            app.logger.info(f"{data['username']} logged in successfully.")
            return jsonify({'access_token': access_token}), 200
        else:
            db.session.rollback()
            app.logger.error(f"Error with loggin in {data['username']}")
            return jsonify({'message': 'Invalid username or password'}), 401
    # create new admin users
    @app.route('/register', methods=['POST'])
    @jwt_required()  
    def register():
        data = request.json
        username = data['username']
        password = data['password']
        # Check if the username is already taken
        existing_user = Admin_users.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username is already taken'}), 400
        # Hash and salt the password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Create a new user and add to the database
        new_user = Admin_users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"{data['username']} logged in successfully.")
        return jsonify({'message': 'User created successfully'}), 201
    
    
