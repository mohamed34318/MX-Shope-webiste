from random import randint

from numpy import ufunc
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Message
from flask import render_template
from sqlalchemy import desc
# Import necessary modules
from flask_mail import Mail, Message
import secrets  # For generating secure tokens
from sqlalchemy.orm import relationship
from sqlalchemy import func
from uuid import uuid4

db = SQLAlchemy()
mail = Mail()

class Customer(db.Model):
    __tablename__ = 'tbl_customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    zip= db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    password_cus = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    
    def __init__(self , id = None ,name = None,email = None,address = None,price = None ,city = None , country = None , zip = None ,status = None ,phone = None ,password_cus = None) :
            self.id= id
            self.name= name
            self.email=email
            self.address=address
            self.city=city
            self.country=country
            self.zip=zip
            self.status=status
            self.phone=phone
            self.password_cus=password_cus
    
    
    def __repr__(self):
        return '<Customer %r>' % self.name
    
    
    def get_customer_data(customer_param) :
       customer_data =  Customer.query.filter_by(email=customer_param.email).first()
       return customer_data
    
    def add_new_customer(customer_param):
        #name, email, address, city, country, zip, phone, password_cus, status
        db.session.add(customer_param)
        db.session.commit()
    
    @staticmethod
    def add_new_customerss(name, email, address, city, country, zip, phone, password, status):
        new_customer = Customer(name=name, email=email, address=address, city=city, country=country, zip=zip, phone=phone, password_cus=password, status=status)
        db.session.add(new_customer)
        db.session.commit()


    def remove_customer(customer_param):
        customer_to_delete = Customer.query.get(customer_param.id)
        if customer_to_delete:
            db.session.delete(customer_to_delete)
            db.session.commit()
            
    @staticmethod
    def update_customer_info(customer_param):
        customer = Customer.query.filter_by(email = customer_param.email).first()

        if customer:
            # Update the attributes of the existing customer record
            customer.name = customer_param.name
            customer.email = customer_param.email
            customer.address = customer_param.address
            customer.city = customer_param.city
            customer.country = customer_param.country
            customer.zip = customer_param.zip
            customer.phone = customer_param.phone
            customer.status = customer_param.status
            # Commit the changes to the database
            db.session.commit()
        else:
            # Handle the case where the customer record is not found
            # For example, you can log an error or raise an exception
            # For now, let's just print an error message
            print("Customer not found for email:", customer_param.email)

    def show_all_customers():
        return Customer.query.all()

    def show_specific_customer(customer_param):
        return Customer.query.get(customer_param.id)
    
    def count_all_customers():
        return Customer.query.count()
    
class Product(db.Model):
    __tablename__ = 'tbl_product'
     
    productId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productName = db.Column(db.String(255), nullable=False)
    catId = db.Column(db.Integer, db.ForeignKey('tbl_category.catId'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category = relationship("Category", back_populates="products")

    def __init__(self , productId = None ,productName = None ,catId = None ,description = None ,price = None  ,image = None,status = None ,quantity = None ) :
        self.productId= productId
        self.productName= productName
        self.catId=catId
        self.description=description
        self.price=price
        self.image=image
        self.status=status
        self.quantity=quantity

    
    
    def __repr__(self):
        return f'<Product {self.productName}>'

    def add_new_product(ProductParam):
        db.session.add(ProductParam)
        db.session.commit()

    def remove_product(ProductParam):
        product_to_delete = Product.query.get(ProductParam.productId)
        if product_to_delete:
            db.session.delete(product_to_delete)
            db.session.commit()
            
    def update_info_product(ProductParam):
        # Validate input parameter
        if not isinstance(ProductParam, Product):
            raise ValueError("Invalid input parameter. Expected Product object.")

        product_to_update = Product.query.get(ProductParam.productId)
        if product_to_update:
            # Update specific attributes if they exist
            for attr, value in ProductParam.items():
                # Skip updating relationships and primary key
                if attr == 'category' or attr == 'productId':
                    continue
                # Check if the attribute exists in the product object
                if hasattr(product_to_update, attr):
                    # Set the attribute value
                    setattr(product_to_update, attr, value)
            # Handle category update if necessary
            if 'category' in ProductParam:
                product_to_update.category = ProductParam.category
            # Commit the changes to the database
            db.session.commit()

            
    def show_products(limit):
      return Product.query.join(Product.category).filter(Category.status == 0).limit(limit).all()

    
    @staticmethod
    def show_products_without_limit():
        # Retrieve all products without any limit
        return Product.query.join(Product.category).filter(Category.status == 0).all()
    @staticmethod
    def show_products_without_limit_admin():
        # Retrieve all products without any limit
        return Product.query.join(Product.category).all()
    
    def show_products_of_specific_productId(product_param):
    # Retrieve the products by name
        products = Product.query.filter_by(productId=product_param.productId).first()
        if products:
            # Retrieve the products associated with the category
            return products
        else:
            # If category not found, return an empty list
            return []
    
    def update_product_status(product_param):
        product = Product.query.filter_by(productId=product_param.productId).first()
        if product:
            if product.quantity <= 0:
                product.status = 1  # Set status to "Out of Stock"
            else:
                product.status = 0  # Set status to "Product still available"
            db.session.commit() 
            
    def update_product(ProductParam):
        if isinstance(ProductParam, dict):
            product = Product.query.get(ProductParam.get('productId'))
            if product:
                product.productName = ProductParam.get('productName')
                product.catId = ProductParam.get('catId')
                product.price = ProductParam.get('price')
                product.quantity = ProductParam.get('quantity')
                product.image = ProductParam.get('image')
                product.status = ProductParam.get('status')
                db.session.commit()
                return product
            else:
                return None
        else:
            raise ValueError("ProductParam must be a dictionary")

    
    def search_products(search_query):
        products = Product.query.filter(Product.productName.ilike(f"%{search_query}%")).join(Product.category).filter(Category.status == 0).all()
        return products

    def get_data_product(product_param) :
       product_data =  Product.query.get(product_param.productId)
       return product_data
    
class Order(db.Model):
    __tablename__ = 'tbl_order'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    productId = db.Column(db.Integer, nullable=False)
    productName = db.Column(db.String(255), nullable=False)  # Include productName attribute
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)
    order_code = db.Column(db.Integer, default=0, nullable=False)
    customerId = db.Column(db.Integer, db.ForeignKey('tbl_customers.id'), nullable=False)
    customer = relationship('Customer', backref='orders')

    def __init__(self,id=None , productId=None, productName=None, quantity=None, price=None, image=None, date=None, status=None  ,order_code = None, customerId=None):
        self.id = id
        self.productId = productId
        self.productName = productName
        self.quantity = quantity
        self.price = price
        self.image = image
        self.date = date
        self.status = status
        self.order_code = order_code
        self.customerId = customerId



    def __repr__(self):
        return f'<Order {self.id}>'

    def make_order(order_param):
        # customerId, productId, productName, quantity, price, image, date, status
        db.session.add(order_param)
        db.session.commit()

    def remove_order(order_param):
        order_to_delete = Order.query.get(order_param.id)  # Assuming order_code is the correct attribute
        if order_to_delete:
            db.session.delete(order_to_delete)
            db.session.commit()

    def update_status_order(order_param):
        order_to_update = Order.query.get(order_param.id)
        if order_to_update:
            order_to_update.status = order_param.status
            db.session.commit()

    def show_orders():
        return Order.query.all()

    def show_customer_order(order_param):
        return Order.query.filter_by(order_code=int(order_param.order_code)).all()
    
    def send_email(order_param, orders, total_cost):
        # Retrieve customer email
        customer_email = Customer.query.get(int(order_param.customerId)).email
        # Compose email message
        msg = Message(subject="Your Order Details",
                    recipients=[customer_email])
        msg.html = render_template('mlemail_template.ht', orders=orders, total_cost=total_cost)
        # Send email
        mail.send(msg)
        
    
    def count_orders_by_status(order_param):
        return db.session.query(func.count(Order.id)).filter(Order.status == order_param.status).scalar() or 0

    def count_orders_with_status_0():
        return Order.count_orders_by_status(0)

    def count_orders_with_status_1():
        return Order.count_orders_by_status(1)

    def remove_orderss(order_id):
        order_to_remove = Order.query.get(order_id)
        if order_to_remove:
            db.session.delete(order_to_remove)
            db.session.commit()
            return True
        else:
            return False

    def count_orders_with_status_2():
        return Order.count_orders_by_status(2)
    
    def get_orders_info_with_status_with_all():
        orders = Order.query.all()
        orders_info = []
        for order in orders:
            order_info = {
                'orderId': order.id , 
                'product_name': order.productName,
                'amount': order.quantity,
                'total_price': f'{order.price}$',
                'email': order.customer.email,
                'customer_name': order.customer.name,
                'status': order.status
            }
            orders_info.append(order_info)
        return orders_info
    
    def get_orders_info_with_status_order_id(order_param):
        order = Order.query.filter_by(customerId = order_param.customerid).first()
        order_info = {
            'product_name': order.productName,
            'amount': order.quantity,
            'total_price': f'{order.price}$',
            'email': order.customer.email,
            'customer_name': order.customer.name,
            'status': order.status
        }
        return order_info

    @staticmethod
    def get_orders_info_with_all_status():
        orders_info = []
        orders = Order.query.all()
        for order in orders:
            if order.customer:  # Check if customer exists
                order_info = {
                'orderId' : order.id   ,                 
                'product_name': order.productName,
                'amount': order.quantity,
                'total_price': f'{order.price}$',
                'email': order.customer.email,
                'customer_name': order.customer.name,
                'status': order.status
                    # Add other order information as needed
                }
                orders_info.append(order_info)
        return orders_info


class Wishlist(db.Model):
    __tablename__ = 'tbl_wlist'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cmrId = db.Column(db.Integer, nullable=False)
    productId = db.Column(db.Integer, nullable=False)


    def __init__(self,id= None,cmrId = None,productId= None  ) :
        self.id= id
        self.cmrId=cmrId
        self.productId=productId


    def __repr__(self):
        return f'<Wishlist {self.id}>'

    def check_wishlist_data(customer_id) :
        wishlist_data_exist = Wishlist.query.filter_by(cmrId = customer_id).all()
        return bool(wishlist_data_exist)

    def add_product_to_wishlist(wishlist_param):
        db.session.add(wishlist_param)
        db.session.commit()

    def remove_product_from_wishlist(wishlist_param):
        wishlist_item_to_delete = Wishlist.query.filter_by(productId = wishlist_param.productId).first()
        if wishlist_item_to_delete:
            db.session.delete(wishlist_item_to_delete)
            db.session.commit()

    def show_products_wishlist(wishlist_param):
        return Wishlist.query.filter_by(cmrId=wishlist_param.cmrId).all()
    
    def show_products_wishlists():
        return Wishlist.query.all()

class Category(db.Model):
    __tablename__ = 'tbl_category'
    catId = db.Column(db.Integer, primary_key=True, nullable=False)
    catName = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    products = relationship("Product", back_populates="category")

    def __init__(self,catId= None,catName= None  , status = None) :
        self.catId= catId
        self.catName=catName
        self.status=status

    def __repr__(self):
        return f'<Category {self.catName}>'

    def add_new_category(category_param):
        new_category = Category(catName=category_param.catName)
        db.session.add(new_category)
        db.session.commit()

    def remove_category(category_param):
        category_to_delete = Category.query.get(category_param.catId)
        if category_to_delete:
            db.session.delete(category_to_delete)
            db.session.commit()

    def update_info_category(category_param):
        category_to_update = Category.query.get(category_param.catId)
        if category_to_update:
            category_to_update.catName = category_param.new_catName
            category_to_update.status = category_param.status
            db.session.commit()

    def show_categories():
        categories = Category.query.all()
        return [category.catName for category in categories]
           
    def show_categories_all():
        categories = Category.query.fitler_by(status=0).all()
        return categories
    
    def show_categories_all_admin():
        categories = Category.query.all()
        return categories
    
    def show_categories_with_product_count_admin():
        categories_with_count = db.session.query(Category, db.func.count(Product.productId)).outerjoin(Product, Category.catId == Product.catId).group_by(Category.catName).all()
        return categories_with_count


    
    def show_categories_with_product_count():
        categories_with_count = db.session.query(Category.catName, db.func.count(Product.productId)).outerjoin(Product, Category.catId == Product.catId).filter(Category.status == 0).group_by(Category.catName).all()
        return categories_with_count

        
    def show_categories_for_home():
        categories = Category.query.filter_by(status=0).all()
        return categories

    def show_products_of_specific_category(category_param):
        # Retrieve the category by name
        category = Category.query.filter_by(catName=category_param.catName, status=0).first()
        if category:
            # Retrieve the products associated with the category
            return category.products
        else:
            # If category not found or has status = 1, return an empty list
            return []
            
class Cart(db.Model):
    __tablename__ = 'tbl_cart'
    cartId = db.Column(db.Integer, primary_key=True, nullable=False)
    customerId = db.Column(db.Integer, nullable=False)
    productId = db.Column(db.Integer, nullable=False)
    productName = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)


    def __init__(self,cartId= None,customerId= None,productId = None,productName= None ,price= None  , quantity= None , image= None) :
        self.catId= cartId
        self.customerId=customerId
        self.productId=productId
        self.productName=productName
        self.price=price
        self.quantity=quantity
        self.image=image


    def __repr__(self):
        return f'<Cart {self.cartId}>'


    def check_cart_data(customerid):
    # Query the cart table to check if it has data
        cart_data = Cart.query.filter_by(customerId = customerid).all()
        return bool(cart_data) 

    def get_cart_data(customer_data) :
        cart_data = Cart.query.filter_by(customerId=customer_data.id).first()
        return cart_data
    
    def add_product_to_cart(cart_param):
        # customerId, productId, productName, price, quantity, image
        db.session.add(cart_param)
        db.session.commit()

    def show_all_products_in_cart():
        return Cart.query.all()

    def show_customers_products_in_cart(cart_param):
        return Cart.query.filter_by(customerId=cart_param.customerId).all()


    def show_specific_cart(cart_param):
        return Cart.query.filter_by(cartId=cart_param.cartId).all()

    def remove_product_from_cart(cart_param):
        cart_item_to_delete = Cart.query.get(cart_param.cartId)
        if cart_item_to_delete:
            db.session.delete(cart_item_to_delete)
            db.session.commit()
            
    def calculate_total_cost(cart_param):
        customer_carts = Cart.query.filter_by(customerId=cart_param.customerId).all()
        total_cost = sum(cart_item.price * cart_item.quantity for cart_item in customer_carts)
        return total_cost

 


    def calculate_total_price_and_quantities(cart_param):
        customer_carts = Cart.query.filter_by(customerId=cart_param.customerId).all()
        total_cost = sum(cart_item.price for cart_item in customer_carts)
        total_quantity = sum(cart_item.quantity for cart_item in customer_carts)
        return total_cost , total_quantity


    def update_info_product_from_cart(cart_param):
        cart_item_to_update = Cart.query.get(cart_param.cartId)
        if cart_item_to_update:
            cart_item_to_update.quantity = cart_param.quantity
            db.session.commit()
    
class Admin(db.Model):
    __tablename__ = 'tbl_admin'
    adminId = db.Column(db.Integer, primary_key=True, nullable=False)
    adminName = db.Column(db.String(50), nullable=False)
    adminUser = db.Column(db.String(50), nullable=False)
    adminEmail = db.Column(db.String(120), nullable=False)  # Add the email column here
    adminPass = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    
    def __init__(self,adminId= None,adminName= None,adminUser= None ,adminEmail = None,adminPass= None  , status= None ) :
        self.adminId= adminId
        self.adminName=adminName
        self.adminUser=adminUser
        self.adminEmail=adminEmail
        self.adminPass=adminPass
        self.status=status

    def __repr__(self):
        return f'<Admin {self.adminName}>'

    def add_new_admin(admin_param):
        # adminName, adminUser, email, adminPass, status
        db.session.add(admin_param)
        db.session.commit()

    def update_admin_information(admin_param):
        admin_to_update = Admin.query.get(admin_param.adminId)
        if admin_to_update:
            # Iterate over the attributes of the admin_param object
            for attr, value in admin_param.__dict__.items():
                # Skip if attribute is adminId or any other attribute not intended for update
                if attr == 'adminId' or not hasattr(admin_to_update, attr):
                    continue
                # Set the attribute value
                setattr(admin_to_update, attr, value)
            # Commit the changes to the database
            db.session.commit()


    def remove_admin(admin_param):
        admin_to_delete = Admin.query.get(admin_param.adminId)
        if admin_to_delete:
            db.session.delete(admin_to_delete)
            db.session.commit()

    
    def show_admins():
        return Admin.query.all()

class Notification:
    def __init__(self, mail):
        self.mail = mail

    def notify_customer_order_placed(self, customer_email, cart_items):
        subject = "Order Placed"
        body = render_template("order_placed_email.html", cart_items=cart_items)
        self.send_email(customer_email, subject, body)

    def notify_customer_order_delivered(self, customer_email, order_id):
        subject = "Order Delivered"
        body = render_template("order_delivered_email.html", order_id=order_id)
        self.send_email(customer_email, subject, body)

    def send_email(self, recipient, subject, body):
        msg = Message(subject, recipients=[recipient])
        msg.html = body
        self.mail.send(msg)

class LoginRegistration(Customer):
    
    def __init__(self):
        self.verification_otp = {} 
        
    def login(self, email, password):
        # Check if the email exists in the database
        customer = self.query.filter_by(email=email).first()
        if customer:
            # Check if the password matches
            if customer.password_cus == password :
                return True, "Login successful."
            else:
                return False, "Incorrect password."
        else:
            return False, "Email not found. Please sign up or check your email."

   
    def signup(self, name, email, address, city, country, zip_code, phone, password):
        # Check if the email already exists in the database
        existing_customer = self.query.filter_by(email=email).first()
        if existing_customer:
            return False, "Email already exists. Please use a different email."
        else:
            # Create a new customer account
            Customer.add_new_customerss(name, email, address, city, country, zip_code, phone, password, 0)  # Assuming status is set to 1 upon registration
            return True, "Signup successful. You can now log in."
        
    def send_verification_code(self, email):
        otp = randint(100000, 999999)  # Ensure OTP is a 6-digit number
        sender = "noreply@example.com"
        msg = Message(subject='OTP', sender=sender, recipients=[email])
        msg.body = str(otp)
        mail.send(msg)
        # Store the OTP along with the email address
        self.verification_otp[email] = otp
        return otp, self.verification_otp  # Return the OTP generated for validation

    def verify_otp(self, email, user_otp):
        # Get stored OTP for the given email
        stored_otp = self.verification_otp.get(email)
        if stored_otp is not None and int(stored_otp) == int(user_otp):
            # OTP is correct
            return True, "OTP verification successful."
        else:
            return False, "Incorrect OTP." 
   
    def updated_password(self, email, new_password):
        customer = self.query.filter_by(email=email).first()
        if customer:
            customer.password_cus = new_password
            db.session.commit()
            return True, "Password updated successfully."
        else:
            return False, "Email not found."
 
class Feedbacks(db.Model):
    __tablename__ = 'feedbacks'
    feed_id = db.Column(db.Integer, primary_key=True, nullable=False)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    feedback_description = db.Column(db.String(120), nullable=False)
    
    def __init__(self , feed_id= None , cust_id = None, feedback_description= None) :
        self.feed_d = feed_id
        self.cust_id = cust_id
        self.feedback_description = feedback_description

    def __repr__(self):
        return f'<Feedback {self.feed_id}>'

    
    def add_feedback(feedback_param):
        # cust_id, feedback_description
        db.session.add(feedback_param)
        db.session.commit()

    def remove_feedback(feedback_param):
        feedback_to_delete = Feedbacks.query.get(feedback_param.feed_id)
        if feedback_to_delete:
            db.session.delete(feedback_to_delete)
            db.session.commit()

    
    def show_feedbacks():
        return Feedbacks.query.all()

    