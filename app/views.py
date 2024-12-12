from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db, bcrypt
from app.models import Item
from app.forms import RegistrationForm, LoginForm
from app.models import User, Cart, Order, OrderDetails

@app.route('/shop')
def shop():
    items = Item.query.all()  
    user = User.query.filter_by(email=session.get('email')).first()  # Fetch the logged-in user
    return render_template('shop.html', items=items, user=user)

@app.route('/', endpoint='index') 
def home():
    return render_template('index.html')


@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/lookbook') 
def lookbook():
    return render_template('lookbook.html')

@app.route('/messages') 
def messages():
    return render_template('messages.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'logged_in' in session:
        return redirect(url_for('account'))  # Redirect to account.html if logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): 

            session['email'] = form.email.data 

            session['logged_in'] = True
            flash(f'Welcome, {form.email.data}! You are logged in.', 'success')
            return redirect(url_for('account'))  # Redirect to account page
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            # No need to redirect here, the error message will be displayed on the same page
    return render_template('profile.html', form=form) 


@app.route('/account')
def account():
    """Display account details and order history."""
    # Check if the user is logged in
    if 'logged_in' not in session:
        flash("You need to log in to access your account.", "danger")
        return redirect(url_for('profile'))  # Redirect to login page if not logged in

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('profile'))  # Redirect to profile (login) page if user doesn't exist

    # Fetch user's order history
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.order_date.desc()).all()

    return render_template('account.html', user=user, orders=orders)

@app.route('/myorders')
def myorders():
    """Display user's order history."""
    if 'logged_in' not in session:
        flash("You need to log in to view your orders.", "danger")
        return redirect(url_for('profile'))

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('profile'))

    orders = Order.query.filter_by(user_id=user.id).order_by(Order.order_date.desc()).all()
    return render_template('myorders.html', orders=orders)


# use this code when db is reset 
# @app.route('/account')
# def account():
#     if 'logged_in' in session:
#         return render_template('account.html')  # Render account details page
#     else:
#         return redirect(url_for('profile'))  # Redirect to login/create account page

@app.route('/sign_out')
def sign_out():
    session.pop('logged_in', None)  # Clear session data
    return redirect(url_for('index'))


@app.route('/search_results')
def search_results():
    query = request.args.get('q', '')
    results = []  # Initialize results as an empty list
    if query:  # Only search if there is a query
        results = Item.query.filter(Item.name.ilike(f'%{query}%')).all()
    return render_template('search_results.html', results=results, query=query)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        
        session['logged_in'] = True  # Set session variable
        flash(f'Hello {form.name.data}, Thanks for registering', 'success')
        return redirect(url_for('profile'))  # Redirect to profile page

    return render_template('create_account.html', form=form, title="Registration page")


# ------------ CART ---------------

@app.route('/cart')
def cart():
    """Display user's cart."""
    if 'logged_in' not in session:
        flash("You need to log in to view your cart.", "danger")
        return redirect(url_for('profile'))

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('profile'))

    cart_items = Cart.query.filter_by(user_id=user.id).all()
    cart_subtotal = calculate_cart_subtotal(user.id)  # Calculate subtotal
    return render_template('cart.html', cart_items=cart_items, cart_subtotal=cart_subtotal)

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    """Add an item to the user's cart."""
    if 'logged_in' not in session:
        flash("You need to log in to add items to the cart.", "danger")
        return redirect(url_for('profile'))

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()
    item = Item.query.get_or_404(item_id)

    # Check if stock is available
    if item.stock < 1:
        flash(f"'{item.name}' is out of stock.", "danger")
        return redirect(url_for('shop'))

    # Check if item is already in the cart
    cart_entry = Cart.query.filter_by(user_id=user.id, item_id=item.id).first()
    if cart_entry:
        # Only allow adding up to the available stock
        if cart_entry.quantity < item.stock:
            cart_entry.quantity += 1
            item.stock -= 1  # Reduce stock
        else:
            flash(f"You can't add more than {item.stock} of '{item.name}' to your cart.", "danger")
    else:
        cart_entry = Cart(user_id=user.id, item_id=item.id, quantity=1)
        item.stock -= 1  # Reduce stock
        db.session.add(cart_entry)

    db.session.commit()
    flash(f"{item.name} added to your cart.", "success")
    return redirect(url_for('shop'))

@app.route('/update_cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    """Update item quantity in the user's cart."""
    if 'logged_in' not in session:
        flash("You need to log in to modify your cart.", "danger")
        return redirect(url_for('profile'))

    try:
        new_quantity = int(request.form.get('quantity', 0))
        if new_quantity < 0:
            raise ValueError("Invalid quantity")
    except ValueError:
        flash("Invalid quantity.", "danger")
        return redirect(url_for('cart'))

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('cart'))

    cart_item = Cart.query.filter_by(user_id=user.id, item_id=item_id).first()
    if not cart_item:
        flash("Item not found in cart.", "danger")
        return redirect(url_for('cart'))

    # Calculate stock adjustment
    stock_adjustment = cart_item.quantity - new_quantity

    # Check if enough stock is available
    if new_quantity > cart_item.item.stock + cart_item.quantity:
        flash(f"Only {cart_item.item.stock + cart_item.quantity} units of '{cart_item.item.name}' are available.", "danger")
        return redirect(url_for('cart'))

    # Update stock and cart item quantity
    cart_item.item.stock += stock_adjustment
    cart_item.quantity = new_quantity
    db.session.commit()

    flash("Cart updated successfully.", "success")
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    """Remove an item from the user's cart."""
    if 'logged_in' not in session:
        flash("You need to log in to modify your cart.", "danger")
        return redirect(url_for('profile'))

    cart_entry = Cart.query.get_or_404(cart_id)

    # Return stock to the item
    cart_entry.item.stock += cart_entry.quantity

    db.session.delete(cart_entry)
    db.session.commit()
    flash("Item removed from your cart.", "success")
    return redirect(url_for('cart'))  # Redirect back to the cart page


def calculate_cart_subtotal(user_id):
    """Helper function to calculate the subtotal for a user's cart."""
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    subtotal = sum(item.quantity * item.item.price for item in cart_items)
    return round(subtotal, 2)  # Round to 2 decimal places


# ---------------- CHECKOUT --------------------
from datetime import datetime

@app.route('/checkout', methods=['POST'])
def checkout():
    """Process a fake checkout and create an order."""
    if 'logged_in' not in session:
        flash("You need to log in to checkout.", "danger")
        return redirect(url_for('profile'))

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('cart'))

    # Retrieve cart items
    cart_items = Cart.query.filter_by(user_id=user.id).all()
    if not cart_items:
        flash("Your cart is empty. Add items to checkout.", "warning")
        return redirect(url_for('cart'))

    # Create a new order
    new_order = Order(
        user_id=user.id,
        order_date=datetime.now(),
        status="Processing"
    )
    db.session.add(new_order)
    db.session.commit()

    # Move items from cart to order details
    for cart_item in cart_items:
        order_detail = OrderDetails(
            order_id=new_order.id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity
        )
        db.session.add(order_detail)

        # Cart items should already have reduced stock during add-to-cart
        # If not, ensure item stock reduction here:
        # cart_item.item.stock -= cart_item.quantity

        # Remove the cart item
        db.session.delete(cart_item)

    db.session.commit()

    flash("Your order has been placed successfully!", "success")
    return redirect(url_for('profile'))


# ---------------- CANCEL ORDER --------------------

@app.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    """Cancel an order and update item stock."""
    if 'logged_in' not in session:
        flash("You need to log in to cancel an order.", "danger")
        return redirect(url_for('profile'))

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('profile'))

    order = Order.query.filter_by(id=order_id, user_id=user.id).first()

    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('account'))

    # Update stock for each item in the order
    for detail in order.order_details:
        item = detail.item
        item.stock += detail.quantity

    # Remove the order
    db.session.delete(order)
    db.session.commit()

    flash("Your order has been cancelled successfully.", "success")
    return redirect(url_for('account'))






# ---------------- FAVORITES --------------------

@app.route('/favorites')
def favorites():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['email']).first()
    if user:  # Check if user exists
        favorite_items = user.favorite_items
        return render_template('favorites.html', favorite_items=favorite_items)
    else:
        flash('User not found.', 'danger')  # Or handle the error appropriately
        return redirect(url_for('account'))


@app.route('/toggle_favorite/<int:item_id>', methods=['POST'])
def toggle_favorite(item_id):
    if 'email' not in session:
        return jsonify(success=False, message="User not logged in"), 403
    
    user = User.query.filter_by(email=session['email']).first()
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify(success=False, message="Item not found"), 404
    
    if item in user.favorite_items:
        user.favorite_items.remove(item)  # Remove from favorites
        is_favorite = False
    else:
        user.favorite_items.append(item)  # Add to favorites
        is_favorite = True

    db.session.commit()
    return jsonify(success=True, is_favorite=is_favorite)

@app.route('/get_favorite_count')
def get_favorite_count():
    count = 0
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:  # Check if user exists
            count = len(user.favorite_items)
    return jsonify(count=count)