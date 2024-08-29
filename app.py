# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify, request, abort
import datetime
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Import Flask app and SQLAlchemy instance from config
from config import app, db
from models import User, Order

#Initialize JWT _ flask Extension 
jwt = JWTManager(app)
# app = Flask(__name__)

# Define route for user registration
@app.route('/user-register', methods=['POST'])
def userRegister():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # is_customer = data.get('is_customer')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, password, and user type are required.'}), 400
    
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({'error': 'Username already exists. Please choose a different one.'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(
        username=username, 
        email=email, 
        password=hashed_password,
        is_customer=True,
        is_cleaner=False
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully. Please log in.'}), 201

# Define route for cleaner registration
@app.route('/cleaner-register', methods=['POST'])
def cleanerRegister():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # is_customer = data.get('is_customer')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, password, and user type are required.'}), 400
    
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({'error': 'Username already exists. Please choose a different one.'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(
        username=username, 
        email=email, 
        password=hashed_password,
        is_cleaner=True,
        is_customer=False
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully. Please log in.'}), 201

# Define route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if user exists
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={
            'id': user.id, 
            'is_customer': user.is_customer, 
            'is_cleaner': user.is_cleaner,
            'is_admin': user.is_admin
            })
        return jsonify({
            'message': 'Login successful.', 
            'access_token': access_token, 
            'id': user.id, 
            'is_customer': user.is_customer, 
            'is_cleaner': user.is_cleaner,
            'is_admin': user.is_admin
            }), 200
    return jsonify({'error': 'Invalid username or password. Please try again.'}), 401

# Define route for creating order
@app.route('/orders', methods=['GET'])
def all_orders():
    orders_data = Order.query.all()

    # Serialize the orders data
    orders = [{
        'id': order.id,
        'location':{
            'latitude': order.latitude,
            'longitude': order.longitude
        },
        'address': order.address,
        'service_time': order.service_time,
        'status': order.status,
        'created_at': order.created_at,
        'updated_at': order.updated_at,
        'customer': {
            'id': order.customer.id,
            'username': order.customer.username,
            'email': order.customer.email,
            'phone_number': order.customer.phone_number
        },
        'cleaner': {
            'id': order.cleaner.id,
            'username': order.cleaner.username,
            'email': order.cleaner.email,
            'phone_number': order.cleaner.phone_number
        }
    } for order in orders_data]
    return jsonify(orders), 200

# Define route for creating order
@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    latitude=data.get('latitude')
    longitude=data.get('longitude')
    service_time_str=data.get('service_time')

    customer_id=1
    # cleaner_id=3
    cleaner_id=2

    customer = User.query.get(customer_id)

    if not customer.is_customer:
        return jsonify({"error": "Only customers can place orders."}), 400
   
    # Ensure the customer_id and cleaner_id are not the same
    if customer_id == cleaner_id:
        return jsonify({"error": "Customer and Cleaner cannot be the same person."}), 400
    
    # Parse the service_time from ISO 8601 format
    try:
        service_time = datetime.datetime.fromisoformat(service_time_str)
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use ISO 8601 format."}), 400
    
    # create and save the order...
    new_order = Order(
        customer_id=customer_id,
        cleaner_id=cleaner_id,
        latitude=latitude,
        longitude=longitude,
        service_time=service_time
    )
    
    db.session.add(new_order)
    db.session.commit()
    # return new_order
    return jsonify({"message": "Order created successfully"}), 201

# Define route for cancelling an order
@app.route('/cancel-order/<int:order_id>', methods=['PUT'])
def cancel_order(order_id):
    customer_id=2
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    print(f'Customer ID: {order.customer.id}')
    if customer_id != order.customer.id:
        return jsonify({"error": "You are not allowed to cancel this order"}), 401
    
    order.status = 'cancelled'
    db.session.commit()

    return jsonify({"message": "Order cancelled successfully"}), 200

# Define route for Delivering an order
@app.route('/deliver-order/<int:order_id>', methods=['PUT'])
def deliver_order(order_id):
    cleaner_id=2
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    if order.status == 'cancelled':
        return jsonify({"error": "Cancelled Order cannot be delivered"}), 401
    
    if order.status == 'delivered':
        return jsonify({"error": "Order has already been delivered"}), 401
    
    print(f'Cleaner ID: {order.cleaner.id}')
    if cleaner_id != order.cleaner.id:
        return jsonify({"error": "You are not allowed to deliver this order"}), 401
    
    order.status = 'delivered'
    db.session.commit()

    return jsonify({"message": "Order delivered successfully"}), 200

# Route to get all orders belonging to a specific user
@app.route('/my-orders', methods=['GET'])
def get_user_orders():
    user_id =5
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user and user.is_customer:
        # Get all orders associated with the customer
        orders_data = Order.query.filter_by(customer_id=user_id).all()

        # Serialize the orders data
        orders = [{
            'id': order.id,
            'location':{
                'latitude': order.latitude,
                'longitude': order.longitude
            },
            'address': order.address,
            'service_time': order.service_time,
            'status': order.status,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'cleaner': {
                'id': order.cleaner.id,
                'username': order.cleaner.username,
                'email': order.cleaner.email,
                'phone_number': order.cleaner.phone_number
            }
        } for order in orders_data]
        return jsonify(orders), 200

    if user and user.is_cleaner:
        # Get all orders associated with the cleaner
        orders_data = Order.query.filter_by(cleaner_id=user_id).all()

        # Serialize the orders data
        orders = [{
            'id': order.id,
            'location':{
                'latitude': order.latitude,
                'longitude': order.longitude
            },
            'address': order.address,
            'service_time': order.service_time,
            'status': order.status,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'customer': {
                'id': order.customer.id,
                'username': order.customer.username,
                'email': order.customer.email,
                'phone_number': order.customer.phone_number
            }
        } for order in orders_data]
        return jsonify(orders), 200

@app.route('/')
def hello_world():
    currentTime = datetime.datetime.now()
    weekFromNow = datetime.timedelta(days=7)
    expectedRepaymentDate= currentTime+weekFromNow
    return f'Hello World: {expectedRepaymentDate}'

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
