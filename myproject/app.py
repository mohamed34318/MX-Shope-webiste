
from flask import Flask , render_template
from requests import session
from Classes import db, Customer, LoginRegistration, Product, Order, Wishlist, Category, Cart, Admin, Notification, Feedbacks
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message
from flask_mail import Mail
from Classes import db
from sqlalchemy import desc
from statistics import quantiles
from fileinput import filename
from werkzeug.utils import secure_filename
from fileinput import filename
from flask import url_for,redirect,request , flash
from random import randint
from datetime import datetime
from flask import session
from flask import request
from uuid import uuid4
import os
from werkzeug.utils import secure_filename
from flask import flash
from flask import session



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6696933:lA9YknLCjX@sql6.freemysqlhosting.net/sql6696933?charset=utf8mb4'
db.init_app(app)
mail=Mail(app)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/uploads/img'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='email@gmail.com'
app.config['MAIL_PASSWORD']='password' #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


mail.init_app(app)
otp=randint(000000,999999)
# Set the secret key for session management
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def test():
    return "hello orignial "


#*************************************************
#Login
#*************************************************@
login_manager = LoginRegistration()  # Create an instance of LoginRegistration
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, message = login_manager.login(email, password)
        
        # Check if the login was successful
        if success:
            # Check the status of the user
            user = Customer.query.filter_by(email=email).first()
            if user.status == 1:
                # User has status 1, so redirect with an error message
                return render_template('login.html', error="Your account is disabled.")
            else:
                # Store user's email in session upon successful login
                session['email'] = email
                # Redirect to the main page or another route upon successful login
                return redirect(url_for("home_page_with_login"))
        elif Admin.query.filter_by(adminEmail=email, adminPass=password).first():
            # Store admin's email in session upon successful login
            session['email'] = email
            return redirect(url_for("home_admin"))
        else:
            return render_template('login.html', error=message)
    else:
        # Render the login form
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        zip = request.form.get('zip')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Validate form data (example: check if required fields are filled)
        if not name or not email or not password:
            error_message = "Please fill in all required fields."
            return render_template('signup.html', error=error_message)
        
        # Call the signup method of LoginRegistration class
        success, message = login_manager.signup(name, email, address, city, country, zip, phone, password)
        
        if success:
            # Store user's email in session upon successful signup
            session['email'] = email
            flash('Signup successful! You are now logged in.', 'success')
            # Redirect to the signup success page
            return redirect(url_for('signup_success'))
        else:
            # Display an error message on the signup page
            flash(message, 'error')
            return render_template('signup.html')
    else:
        # Render the signup form
        return render_template('signup.html')

@app.route('/signup/success')
def signup_success():
    return render_template('signup_success.html')
#*************************************************


#*************************************************
#Home Pages
#*************************************************

@app.route('/base_page')
def base_page():
    # Retrieve customer email from session
    email = session.get('email')
    if email:
        # Fetch customer data
        customer_data = Customer.query.filter_by(email=email).first()
        if customer_data:
            # Fetch category names and product counts from the database
            Categories_count = Category.show_categories_with_product_count()
            products = Product.show_products(limit=5)
            cart_data = Cart.check_cart_data(customer_data.id)
            return render_template("base_page.html"  , cart_data = cart_data, Categories_count=Categories_count, customer_data=customer_data, products=products)
        else:
            # Handle the case where the customer with the provided email does not exist
            return "Customer not found", 404
    else:
        # Handle the case where the customer is not logged in
        return "Unauthorized", 401

@app.route('/home')
def home_page():
    # Fetch category names and product counts from the database
    Categories_count = Category.show_categories_with_product_count()
    products = Product.show_products(limit=5)

    return render_template("index.html", Categories_count=Categories_count, products=products)

@app.route('/home_page_with_login')
def home_page_with_login():
    # Retrieve customer email from session
    email = session.get('email')
    if email:
        # Fetch customer data
        customer_data = Customer.query.filter_by(email=email).first()
        if customer_data:
            # Fetch category names and product counts from the database
            Categories_count = Category.show_categories_with_product_count()
            products = Product.show_products(limit=5)
            cart_data = Cart.check_cart_data(customer_data.id)
            wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
            return render_template("Page_with_login.html"  , wishlist_data_exists = wishlist_data_exists, cart_data = cart_data, Categories_count=Categories_count, customer_data=customer_data, products=products)
        else:
            # Handle the case where the customer with the provided email does not exist
            return "Customer not found", 404
    else:
        # Handle the case where the customer is not logged in
        return "Unauthorized", 401

@app.route('/home_page_with_logins')
def home_page_with_logins():
    # Retrieve customer email from session
    email = session.get('email')
    if email:
        # Fetch customer data
        customer_data = Customer.query.filter_by(email=email).first()
        if customer_data:
            # Fetch category names and product counts from the database
            Categories_count = Category.show_categories_with_product_count()
            products = Product.show_products(limit=5)
            cart_data = Cart.check_cart_data(customer_data.id)
            wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
            return render_template("Page_with_login.html",wishlist_data_exists = wishlist_data_exists , cart_data = cart_data , Categories_count=Categories_count, customer_data=customer_data, products=products)
        else:
            # Handle the case where the customer with the provided email does not exist
            return "Customer not found", 404
    else:
        # Handle the case where the customer is not logged in
        return "Unauthorized", 401

@app.route('/show_customer_data_edit', methods=["GET", "POST"])
def show_customer_data_edit():
    
    customer_email = session.get('email')
    if request.method == "POST":
        # Process the form data submitted by the user
        # Retrieve form data
        name = request.form.get('name')
        email = customer_email
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        zip_code = request.form.get('zip')  # Corrected variable name
        phone = request.form.get('phone')

        customer_param = Customer(name=name, email=email, address=address, city=city, country=country, zip=zip_code, phone=phone)
        # Update the customer data
        Customer.update_customer_info(customer_param)
        db.session.commit()
        # Redirect the user to the profile page (GET request)
        return redirect(url_for('show_customer_data'))
    
    else :
        # Retrieve customer data to display on the profile page
        customer_email = session.get('email')
        customer_data = Customer(email=customer_email)
        customer_data = Customer.get_customer_data(customer_data)
        return render_template('edit_profile.html', customer_data=customer_data)
     
@app.route('/show_customer_data')
def show_customer_data():
    # Retrieve customer data to display on the profile page
    customer_email = session.get('email')
    customer_data = Customer(email = customer_email)
    customer_data = Customer.get_customer_data(customer_data)
    return render_template('profile_page.html', customer_data=customer_data)

@app.route('/remove_customers', methods=['POST'])
def remove_customers():
    if request.method == 'POST':
        # Get the customer ID from the form
        customer_id = request.form.get('customer_id')

        # Query the customer from the database
        customer = Customer.query.get(customer_id)

        if customer:
            # Update the status of the customer to closed (status = 1)
            customer.status = 1
            # Customer.remove_customer(customer_data_removed)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            # Handle the case where the customer does not exist
            flash('Customer not found', 'error')
            return redirect(url_for('show_customer_data'))

    # Handle other HTTP methods
    return redirect(url_for('show_customer_data'))

#*************************************************


#*************************************************
#Search Products
#*************************************************
@app.route('/search_product', methods=['GET'])
def search_product():
    search_query = request.args.get('query')
    if 'email' in session:
        email = session['email']
        customer_data = Customer.query.filter_by(email=email).first()
    else:
        customer_data = None
    
    Categories_count = Category.show_categories_with_product_count()
    
    if search_query:
        # Query the database to find products whose names contain the search query
        products = Product.search_products(search_query)
    else:
        # If no search query is provided, return an empty list of products
        products = []
    cart_data = Cart.check_cart_data(customer_data.id)
    wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
    return render_template("search_results.html" , cart_data = cart_data , wishlist_data_exists = wishlist_data_exists, customer_data=customer_data, Categories_count=Categories_count, products=products, search_query=search_query)
#*************************************************


#*************************************************
#verify And validate functions for forgeting password
#*************************************************
def send_email(customer_id, orders, total_cost):
    # Retrieve customer email  
    customer_email = Customer.query.get(customer_id).email
    # Compose email message
    msg = Message(subject="Your Order Details",
                  sender = "aposaad343@gmail.com",
                recipients=[customer_email])
    msg.html = render_template('email_template.html', orders=orders, total_cost=total_cost)
    # Send email
    mail.send(msg) 
 
def send_email_notification(customer_id, order):
    customer = Customer.query.get(customer_id)
    status_map = {1: 'Confirmed', 2: 'Delivered'}
    status = status_map.get(order.status, 'Unknown')
    subject = f"Your Order {order.order_code} ({status} has been changed )"
    message = f"""Dear {customer.name},
    
Your order details:
    
Product Name: {order.productName}
Amount: {order.quantity}
Total Price: {order.price}
status : {status}.
    
Thank you for shopping with us!"""
    msg = Message(subject=subject, sender="aposaad343@gmail.com", recipients=[customer.email], body=message)
    mail.send(msg) 
    
@app.route('/verify', methods=[ "GET", "POST"])
def verify():
    if request.method == "POST":
        email = request.form['email']
        login_registration = LoginRegistration()
        otp , verification_otp = login_registration.send_verification_code(email)
        if otp :
            return render_template('verify.html', email=email , verification_otp = verification_otp)
        else:
            return render_template("enter_email_to_verify.html") + "Failed to send verification code."
    else : 
        return render_template("enter_email_to_verify.html")

@app.route('/validate', methods=['POST'])
def validate():
    if request.method == "POST":
        email = request.form['email']
        user_otp = request.form['otp']
        verification_otp = request.form['verification_otp']
        login_registration = LoginRegistration()
        result, message = login_registration.verify_otp(email, user_otp , verification_otp)
        if result:
            return render_template('update_password.html', email=email)
        else:
            return message

@app.route('/update_password', methods=['POST'])
def update_password():
    if request.method == "POST":
        email = request.form['email']
        new_password = request.form['password']
        login_registration = LoginRegistration()
        result, message = login_registration.updated_password(email, new_password)
        if result:
            return render_template('update_password.html') + "successful updated"
        else:
            return message
    else:
        return "Method Not Allowed"
#*************************************************


#*************************************************
#Products page
#*************************************************
@app.route('/product_page')
def product_page():
    # Retrieve customer data (assuming email is stored in session)
    if 'email' in session:
        email = session['email']
        customer_data = Customer.query.filter_by(email=email).first()
    else:
        customer_data = None
    
    # Retrieve all products
    product_obj = Product()
    products_info = product_obj.show_products_without_limit()
    # random.shuffle(products_info)  # Shuffling products is commented out
    
    # Retrieve category counts
    Categories_count = Category.show_categories_with_product_count()

    # Render the template with products and customer data
    cart_data = Cart.check_cart_data(customer_data.id)
    wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
    return render_template("products_page.html" , cart_data = cart_data ,wishlist_data_exists = wishlist_data_exists , products=products_info, customer_data=customer_data, Categories_count=Categories_count)

@app.route('/category/<category_name>')
def products_page_with_specific_category(category_name):
    # Retrieve customer email from session
    email = session.get('email')
    if email:
        # Fetch customer data
        customer_data = Customer.query.filter_by(email=email).first()
        if customer_data:
            # Retrieve the category based on the provided category name
            category = Category.query.filter_by(catName=category_name).first()
            Categories_count = Category.show_categories_with_product_count()
            if category:
                # Access the products of the category
                category_param = Category(catName=category_name)
                products = Category.show_products_of_specific_category(category_param)
                cart_data = Cart.check_cart_data(customer_data.id)
                wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
                return render_template('category_products.html',cart_data = cart_data , wishlist_data_exists = wishlist_data_exists , Categories_count=Categories_count, category=category, customer_data=customer_data, products=products)
            else:
                return "Category not found", 404
        else:
            # Handle the case where the customer with the provided email does not exist
            return "Customer not found", 404
    else:
        # Handle the case where the customer is not logged in
        return "Unauthorized", 401

@app.route('/product/<int:productid>')
def show_product_details(productid):
    # Retrieve customer data from the session
    if 'email' in session:
        email = session['email']
        customer_data = Customer.query.filter_by(email=email).first()
    else:
        # If customer is not logged in, set customer_data to None
        customer_data = None
    
    # Fetch product data based on the provided product ID
    product = Product.query.get(productid)
    
    # Check if the product exists
    if product:
        # Access the category associated with the product using the relationship
        category = product.category
        
        # Check if the category status is equal to 0
        if category.status == 0:
            # Check if the quantity of the product is greater than 0
            if product.quantity > 0:
                availability_message = "This product is available with a specific quantity."
                add_to_cart_disabled = False
            else:
                availability_message = "This product is out of stock."
                add_to_cart_disabled = True
                # Update product status to "Out of Stock" since quantity is 0
                product.status = 1
                # Update product status in the database
                db.session.commit()
        else:
            availability_message = "This product is out of stock due to category status."
            add_to_cart_disabled = True
            # Update product status to "Out of Stock" since category status is not 0
            product.status = 1
            # Update product status in the database
            db.session.commit()
        cart_data = Cart.check_cart_data(customer_data.id)
        wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
        Categories_count = Category.show_categories_with_product_count()
        # Render the template with product and availability information
        return render_template('detail.html' , cart_data = cart_data ,Categories_count = Categories_count , wishlist_data_exists = wishlist_data_exists, product=product, customer_data=customer_data, availability_message=availability_message, add_to_cart_disabled=add_to_cart_disabled)
        # return f"<h3>this product are closed !</h3>"
    else:
        # Handle case where the product does not exist
        return "Product not found", 404
#*************************************************

#*************************************************
# Cart Shopping pages
#*************************************************
@app.route('/add_to_cart/<int:productid>', methods=['POST'])
def add_to_cart(productid):
    customer_email = session.get('email')
    if not customer_email:
        return redirect(url_for('login'))
    customer_data = Customer.query.filter_by(email=customer_email).first()
    if not customer_data:
        return "Customer not found", 404
    product_data = Product.query.get(productid)
    if not product_data:
        return "Product not found", 404
    
    productName = product_data.productName
    price = product_data.price
    requested_quantity = int(request.form.get('quantity', 1))  
    available_quantity = product_data.quantity

    if requested_quantity <= available_quantity:
        cart_param = Cart(customerId=customer_data.id, productId=productid, productName=productName, price=price, quantity=requested_quantity, image=product_data.image)
        Cart.add_product_to_cart(cart_param)
    cart_data = Cart.check_cart_data(customer_data.id)
    wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
    return redirect(url_for('show_carts' , cart_data = cart_data ,wishlist_data_exists = wishlist_data_exists ))

@app.route('/remove_product_from_cart/<int:productid>', methods=['GET', 'POST'])
def remove_product_from_cart(productid):
    # Retrieve customer email from session
    customer_email = session.get('email')
    customer_data = Customer.query.filter_by(email=customer_email).first()

    # Check if the customer is logged in
    if not customer_email:
        # Handle the case where the customer is not logged in
        return redirect(url_for('login'))

    # Find the product in the cart based on product id and customer id
    product_to_remove = Cart.query.filter_by(customerId=customer_data.id, productId=productid).first()

    # Check if the product exists in the cart
    if product_to_remove:
        db.session.delete(product_to_remove)
        db.session.commit()
        return redirect(url_for('show_carts'))
    else:
        return "Product not found in cart"
    
@app.route('/show_carts')
def show_carts():
    # Retrieve customer email from session
    customer_email = session.get('email')
    
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    
    # Retrieve customer data based on email
    customer_param = Customer(email = customer_email)
    customer_data = Customer.get_customer_data(customer_param)

    # Retrieve category counts
    Categories_count = Category.show_categories_with_product_count()

    # Retrieve cart information for the customer
    customer_param = Customer(id = customer_data.id)
    customer_cart = Cart.get_cart_data(customer_param)
    product_id = customer_cart.productId if customer_cart else None

    # Calculate total prices and quantities
    cart_param = Cart(customerId=customer_data.id)
    total_prices, total_quantity = Cart.calculate_total_price_and_quantities(cart_param)
    total_cost = Cart.calculate_total_cost(cart_param)

    # Retrieve customer carts
    customer_carts = Cart.show_customers_products_in_cart(cart_param)
    cart_data = Cart.check_cart_data(customer_data.id)
    wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
    return render_template('cart.html', cart_data = cart_data , wishlist_data_exists = wishlist_data_exists ,
                           total_prices=total_prices, Categories_count=Categories_count,
                           productid=product_id, total_quantity=total_quantity, total_cost=total_cost,
                           customer_data=customer_data, customer_carts=customer_carts)
#*************************************************



#*************************************************
# Order Pages
#*************************************************
from sqlalchemy import func

@app.route('/order_placed/<int:customerid>')
def place_order(customerid):
    # Retrieve customer email from session
    customer_email = session.get('email')
    
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    
    # Retrieve customer data based on email
    customer_data = Customer.query.filter_by(email=customer_email).first()
    customer_id = customerid
    
    # Retrieve all items in the cart for the customer
    cart_param = Cart(customerId=customer_id)
    customer_carts = Cart.show_customers_products_in_cart(cart_param)

    # Dictionary to hold summed quantities for each product
    summed_quantities = {}
    for cart_item in customer_carts:
        product_id = cart_item.productId
        summed_quantities.setdefault(product_id, 0)
        summed_quantities[product_id] += cart_item.quantity

    # Flag to indicate if any product exceeds available quantity
    exceeds_quantity_flag = False
    for product_id, total_quantity in summed_quantities.items():
        product_data = Product.query.get(product_id)
        if total_quantity > product_data.quantity:
            exceeds_quantity_flag = True
            break  # Exit loop if any product exceeds quantity

    if exceeds_quantity_flag:
        # Flash message indicating exceeding quantity
        flash("The quantities of some items in your order exceed the available quantity.", "error")
        return redirect(url_for('show_carts'))

    else:
        # Retrieve the maximum order code from existing orders
        max_order_code = db.session.query(func.max(Order.order_code)).scalar()
        if max_order_code is None:
            # If there are no existing orders, start from 1
            order_code = 1
        else:
            order_code = max_order_code + 1

        # Proceed with placing orders for all items in the cart with the same order code
        for cart_item in customer_carts:
            product_data = Product.query.get(cart_item.productId)
            # Proceed with placing order
            order = Order(
                customerId=cart_item.customerId,
                productId=cart_item.productId,
                productName=cart_item.productName,
                quantity=cart_item.quantity,
                price=cart_item.price,
                image=cart_item.image,
                date=datetime.now(),  # Assuming you want to use the current date and time
                status=0,  # Assuming status 0 indicates an active order
                order_code=order_code  # Set the same order code for all items in the order
            )
            db.session.add(order)
            # Remove the item from the cart after placing the order
            Cart.remove_product_from_cart(cart_item)  # Pass cart item directly
            # Update product quantity
            product_data.quantity -= cart_item.quantity
            # Update product status
            product_param = Product(productId=int(cart_item.productId))
            Product.update_product_status(product_param)

        # Commit all changes to the database
        db.session.commit()

        # Retrieve orders for the specific customer
        order_param = Order(order_code=order_code)
        customer_orders = Order.show_customer_order(order_param)

        # Calculate the total cost of the orders
        total_cost = 0
        for order in customer_orders:
            total_cost += order.price * order.quantity

        # Send email
        send_email(customer_id, customer_orders, total_cost)

        # Redirect to the confirmation page after placing the order
        return redirect(url_for('order_confirmation', total_cost=total_cost))

@app.route('/order_confirmation')
def order_confirmation():
    # Retrieve customer email from session
    email = session.get('email')
    if email:
        # Fetch customer data
        customer_data = Customer.query.filter_by(email=email).first()
        if customer_data:
            # Render the confirmation page

            return render_template('order_confirmation.html', customer_data=customer_data)
        else:
            # Handle the case where the customer with the provided email does not exist
            return "Customer not found", 404
    else:
        # Handle the case where the customer is not logged in
        return "Unauthorized", 401

@app.route('/remove_order_of_user/<int:order_id>', methods=['POST'])
def remove_order_of_user(order_id):
    # Check if the request is POST
    if request.method == 'POST':
        # Retrieve customer email from session
        customer_email = session.get('email')
        
        # Check if the customer is logged in
        if not customer_email:
            # Redirect to the login page if the customer is not logged in
            return redirect(url_for('login'))
        
        # Retrieve customer data based on email
        customer_data = Customer.query.filter_by(email=customer_email).first()
        
        # Check if customer data exists
        if customer_data:
            # Check if the order belongs to the customer
            order = Order.query.get(order_id)
            if order and order.customerId == customer_data.id:
                # Remove the order
                Order.remove_order(order)
                # Redirect to the orders page
                return redirect(url_for('orders'))
            else:
                # If the order does not exist or does not belong to the customer, redirect to an error page
                return redirect(url_for('error_page'))  # You need to define this route for error handling
        else:
            # If customer data does not exist, redirect to the login page
            return redirect(url_for('login'))

@app.route('/orders')
def orders():
    # Retrieve customer data from the session
    if 'email' in session:
        email = session['email']
        customer_data = Customer.query.filter_by(email=email).first()
    else:
        # If customer is not logged in, set customer_data to None
        customer_data = None
    
    # Retrieve category counts
    Categories_count = Category.show_categories_with_product_count()
    
    # Retrieve recent products to display
    products = Product.show_products(limit=5)
    
    # Retrieve orders associated with the logged-in customer
    if customer_data:
        orders = Order.query.filter_by(customerId=customer_data.id).all()
        # Extract order IDs
        order_ids = [order.id for order in orders]
    else:
        orders = []
        order_ids = []
    cart_data = Cart.check_cart_data(customer_data.id)
    wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
    return render_template('orders.html' , cart_data = cart_data ,wishlist_data_exists = wishlist_data_exists , orders=orders, order_ids=order_ids, customer_data=customer_data, Categories_count=Categories_count, products=products)
#*************************************************

#*************************************************
# Wishlist Pages
#*************************************************
@app.route('/add_to_wishlist/<int:productid>', methods=['POST'])
def add_to_wishlist(productid):
    if request.method == 'POST':
        # Retrieve customer email from session
        email = session.get('email')
        if email:
            # Fetch customer data
            customer_data = Customer.query.filter_by(email=email).first()
            if customer_data:
                # Add product to the wishlist
                wishlist_param = Wishlist(cmrId=customer_data.id, productId=productid)
                Wishlist.add_product_to_wishlist(wishlist_param)
                # Redirect to the wishlist page after adding to wishlist
                return redirect(url_for('show_wishlist'))
            else:
                # Handle the case where the customer with the provided email does not exist
                return "Customer not found", 404
        else:
            # Handle the case where the customer is not logged in
            return "Unauthorized", 401
    else:
        # Handle the case where the request method is not POST
        return "Method Not Allowed", 405

@app.route('/show_wishlist')
def show_wishlist():
    # Retrieve customer email from session
    email = session.get('email')
    if email:
        # Fetch customer data
        customer_data = Customer.query.filter_by(email=email).first()
        if customer_data:
            # Fetch wishlist data for the customer
            wishlist_param = Wishlist(cmrId=customer_data.id)
            wishlist_data = Wishlist.show_products_wishlist(wishlist_param)
            
            # Fetch category information
            Categories_count = Category.show_categories_with_product_count()
            
            # Fetch product information for each item in the wishlist
            wishlist_products = []
            for item in wishlist_data:
                product = Product.query.get(item.productId)
                if product:
                    wishlist_products.append(product)
            
            # Fetch some products for display (optional)
            products = wishlist_products
            cart_data = Cart.check_cart_data(customer_data.id)
            wishlist_data_exists = Wishlist.check_wishlist_data(customer_data.id)
            return render_template('wishlist_page.html' , cart_data = cart_data ,wishlist_data_exists = wishlist_data_exists , wishlist_products=wishlist_products, customer_data=customer_data, Categories_count=Categories_count, products=products)
        else:
            # Handle the case where the customer with the provided email does not exist
            return "Customer not found", 404
    else:
        # Handle the case where the customer is not logged in
        return "Unauthorized", 401

@app.route('/remove_from_wishlist/<int:productid>')
def remove_from_wishlist(productid):
    # Retrieve customer email from session
    email = session.get('email')
    if email:
        # Fetch customer data
        customer_data = Customer.query.filter_by(email=email).first()
        if customer_data:
            # Remove the product from the wishlist
            wishlist_param = Wishlist(cmrId=customer_data.id, productId=productid)
            Wishlist.remove_product_from_wishlist(wishlist_param)
            # Redirect to the wishlist page
            return redirect(url_for('show_wishlist'))
        else:
            # Handle the case where the customer with the provided email does not exist
            return "Customer not found", 404
    else:
        # Handle the case where the customer is not logged in
        return "Unauthorized", 401
#*********************************************************************************************  



#*********************************************************************************************
# admin pages 
#*********************************************************************************************




#*********************************************************************************************
# home pages 
#*********************************************************************************************
@app.route('/Home_admin')
def home_admin():
      # Retrieve customer email from session
    customer_email = session.get('email')
    
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    email = customer_email
    admin_data = Admin.query.filter_by(adminEmail=email).first()
    total_customers = Customer.count_all_customers()
    order_param = Order(status = 0)
    total_order_pending = Order.count_orders_by_status(order_param)
    order_param = Order(status = 1)
    total_order_confirmed = Order.count_orders_by_status(order_param)
    order_param = Order(status = 2)
    total_order_dlevired = Order.count_orders_by_status(order_param)
    
    get_orders_info_with_status_0 = Order.get_orders_info_with_all_status()
    return render_template('Home.html', get_orders_info_with_status_0= get_orders_info_with_status_0 , admin_data=admin_data ,total_order_dlevired = total_order_dlevired , total_order_pending =total_order_pending ,total_order_confirmed = total_order_confirmed  , total_customers = total_customers)

@app.route('/Home_admins/')
def home_admins():
          # Retrieve customer email from session
    customer_email = session.get('email')
    
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=customer_email).first()
    total_customers = Customer.count_all_customers()
    order_param = Order(status = 0)
    total_order_pending = Order.count_orders_by_status(order_param)
    order_param = Order(status = 1)
    total_order_confirmed = Order.count_orders_by_status(order_param)
    order_param = Order(status = 2)
    total_order_dlevired = Order.count_orders_by_status(order_param)
    
    get_orders_info_with_status_0 = Order.get_orders_info_with_status_with_all()
    return render_template('Home.html', get_orders_info_with_status_0= get_orders_info_with_status_0 , admin_data=admin_data ,total_order_dlevired = total_order_dlevired , total_order_pending =total_order_pending ,total_order_confirmed = total_order_confirmed  , total_customers = total_customers)
#*********************************************************************************************


#*********************************************************************************************
# manage Pages
#*********************************************************************************************
@app.route('/manage_user/')
def manage_user():
              # Retrieve customer email from session
    customer_email = session.get('email')
    
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=customer_email).first()
    customer_data = Customer.show_all_customers()
    return render_template('Manage_users.html', customer_data=customer_data, email=customer_email, admin_data=admin_data)

@app.route('/manage_posts')
def manage_posts():
    customer_email = session.get('email')
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=customer_email).first()
    product_data = Product.show_products_without_limit_admin()
    categories = Category.show_categories_all_admin()
    return render_template('Manage_posts.html', product_data=product_data,  admin_data=admin_data   , categories = categories)

@app.route('/manage_orders')
def manage_orders():
    customer_email = session.get('email')
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=customer_email).first()
    order_data = Order.show_orders()
    return render_template('manage_order.html', order_data=order_data, admin_data=admin_data)

@app.route('/manage_category')
def manage_category():
    customer_email = session.get('email')
    # Check if the customer is logged in
    if not customer_email:
        # Redirect to the login page if the customer is not logged in
        return redirect(url_for('login'))
    category_data_admin = Category.show_categories_all_admin()
    return render_template('manage_category.html', category_data_admin=category_data_admin)

#*********************************************************************************************




#*********************************************************************************************
# update Pages
#*********************************************************************************************
@app.route('/modify_user/<int:customerid>', methods=["GET", "POST"])
def update_user(customerid):
    customer_email = session.get('email')
    # Check if the customer is logged in
    if not customer_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        zip_code = request.form.get('zip')
        phone = request.form.get('phone')
        email = request.form.get('email')
        status = request.form.get('status')
        Customer_param = Customer( 
            id=customerid,
            name=name,
            email=email,
            address=address,
            city=city,
            country=country,
            zip=zip_code,
            phone=phone,
            status=status
            )
        Customer.update_customer_info(Customer_param)
        return redirect(url_for("manage_user", email=customer_email))
    else:
        customer_param = Customer(id = customerid)
        customer_data = Customer.show_specific_customer(customer_param)
        return render_template('update_user_page.html', customer_data=customer_data)

@app.route('/modify_post/<int:productid>', methods=["GET", "POST"])
def update_post(productid):
    customer_email = session.get('email')
    # Check if the customer is logged in
    if not customer_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    if request.method == 'POST':
        # Retrieve form data
        productName = request.form.get('productName')
        catId = request.form.get('catId')  # Retrieve catId from the form
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        uploaded_file = request.files.get('image')
        if uploaded_file is not None:
            filename = secure_filename(uploaded_file.filename) 
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        else:
            filename = None  # No file uploaded
        
        status = request.form.get('status')
        
        # Check if form data is not empty
        if productName and catId and price and quantity and status:
            # Update the product
            product_param = {
            'productId': productid,
            'productName': productName,
            'catId': catId,
            'price': price,
            'quantity': quantity,
            'image': filename,  
            'status': status
            }

            updated_product = Product.update_product(product_param)
            if updated_product:
                # Optionally, you can redirect with a success message
                return redirect(url_for("manage_posts"))
            else:
                # Optionally, you can handle the case where the product is not found
                return "Product not found"
        else:
            # Handle case where form data is incomplete
            return "Form data is incomplete"
    else:
        product_data = Product.query.filter_by(productId=productid).first()
        categories = Category.show_categories_all_admin()
        return render_template('update_posts_page.html', product_data=product_data, categories=categories)

@app.route('/update_order_status/<int:order_id>', methods=['GET', 'POST'])
def update_order_status(order_id):
    customer_email = session.get('email')
    # Check if the customer is logged in
    if not customer_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=customer_email).first()
    order = Order.query.get(order_id)
    customer_data = Customer.query.get(order.customerId)  # Fetch customer data using customerId

    if request.method == 'POST':
        new_status = int(request.form['status'])
        if new_status != order.status:
            # Update order status
            order_param = Order(id=order_id, status=new_status)
            Order.update_status_order(order_param)

            # Send email notification if status changes to Confirmed or Delivered
            if new_status in [1, 2]:
                send_email_notification(order.customerId, order)

            return redirect(url_for('manage_orders', email=customer_email, admin_data=admin_data))

    # Render template if request method is not 'POST' or if status is not updated
    return render_template('update_order_page.html', customer_data=customer_data, order=order, email=customer_email)

@app.route('/update_category_data/<int:catId>', methods=['GET', 'POST'])
def update_category_data(catId):
    customer_email = session.get('email')
    # Check if the customer is logged in
    if not customer_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=customer_email).first()
    category_data = Category.query.get(catId)
    
    if request.method == 'POST':
        catName = request.form.get('catName')
        status = request.form.get('status')

        # Update category information
        category_data.catName = catName
        category_data.status = status
        db.session.commit()
        
        return redirect(url_for('manage_category', email=customer_email))

    return render_template('update_category_page.html', Category_data=category_data  , admin_data = admin_data, email=customer_email)

#*********************************************************************************************




#*********************************************************************************************
# remove Pages
#*********************************************************************************************
@app.route('/remove_post/<int:productid>')
def remove_post(productid) : 
    admin_email = session.get('email')
    # Check if the customer is logged in
    if not admin_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=admin_email).first()
    product_param = Product(productId=productid)
    Product.remove_product(product_param)
    return redirect(url_for('manage_posts' , email = admin_email , admin_data = admin_data))   

@app.route('/remove_order/<int:order_id>', methods=['GET', 'POST'])
def remove_order(order_id):
    admin_email = session.get('email')
    # Check if the customer is logged in
    if not admin_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=admin_email).first()
    order_param = Order(id=order_id)
    Order.remove_order(order_param)
    return redirect(url_for('manage_orders', email=admin_email, admin_data=admin_data))

@app.route('/remove_user/<int:customerid>')
def remove_user(customerid) : 
    admin_email = session.get('email')
    # Check if the customer is logged in
    if not admin_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    admin_data = Admin.query.filter_by(adminEmail=admin_email).first()
    customer_param = Customer(id = customerid)
    Customer.remove_customer(customer_param)
    return redirect(url_for('manage_user' , email = admin_email , admin_data = admin_data))

@app.route('/remove_category/<int:category_id>')
def remove_category(category_id ):
    admin_email = session.get('email')
    # Check if the customer is logged in
    if not admin_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    category_data = Category(catId=category_id)
    Category.remove_category(category_data)
    return redirect(url_for('manage_category' ,email = admin_email))
#*********************************************************************************************



#*********************************************************************************************
# Add Pages in Admin
#*******************************************************************************************
@app.route('/add_post', methods=["GET", "POST"])
def add_post():
    admin_email = session.get('email')
    # Check if the customer is logged in
    if not admin_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    if request.method == 'POST':
        # Retrieve form data
        productName = request.form.get('productName')
        catId = request.form.get('catId')  # Retrieve catId from the form
        description = request.form.get('description')
        price = request.form.get('price')
        uploaded_file = request.files.get('productImage')
        status = request.form.get('status')
        quantity = request.form.get('quantity')

        # Validate form data
        if productName and catId and description and price and status and quantity:
            # Check if price is valid
            if price.isdigit():
                # Convert price to float
                price = float(price)
                filename = None
                if uploaded_file:
                    filename = secure_filename(uploaded_file.filename)
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                # Create a new product instance
                productx = Product(
                    productName=productName,
                    catId=catId,
                    description=description,
                    price=price,
                    image=filename,
                    status=status,
                    quantity=quantity
                )
                # Add the product to the database
                Product.add_new_product(productx)
                # Redirect to the manage_posts route
                return redirect(url_for("manage_posts"))
            else:
                return "Invalid price format. Please enter a valid price."
        else:
            return "Form data is incomplete"
    else:
        categories = Category.show_categories_all_admin()
        return render_template('add_post_page.html', categories=categories)

@app.route('/add_category', methods=["GET", "POST"])
def add_category():
    admin_email = session.get('email')
    # Check if the customer is logged in
    if not admin_email:
    # Redirect to the login page if the customer is not logged in
         return redirect(url_for('login'))
    if request.method == 'POST':

        catName = request.form.get('catName')
        status = request.form.get('status')
        category_param = Category(
            catName=catName,
            status = status
        )
        # Add the product to the database
        new_category = Category(catName=category_param.catName , status =category_param.status )
        db.session.add(new_category)
        db.session.commit()
        # Redirect to the manage_posts route
        return redirect(url_for("manage_category"))
    else:
        categories = Category.show_categories_all_admin()
        return render_template('add_category_page.html', categories=categories)
#*********************
if __name__ == '__main__':
     app.run(debug=True)
     