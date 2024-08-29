from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Define User model
class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_customer = db.Column(db.Boolean, default=False, nullable=False)
    is_cleaner = db.Column(db.Boolean, default=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    farm_name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True) 

    # Relationship with Order model as a customer
    customer_orders = db.relationship('Order', foreign_keys='Order.customer_id', backref='customer', lazy=True)
    
    # Relationship with Order model as a cleaner
    cleaner_orders = db.relationship('Order', foreign_keys='Order.cleaner_id', backref='cleaner', lazy=True)

# Define Order model
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys for customer and cleaner
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cleaner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Store latitude and longitude for location data
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Optional: Store a human-readable address
    address = db.Column(db.String(255), nullable=True)
    # is_delivered = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    service_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Add a check constraint to ensure customer_id and cleaner_id are not the same
    __table_args__ = (
        db.CheckConstraint('customer_id != cleaner_id', name='check_customer_cleaner_different'),
    )
