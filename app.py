from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Product, CartItem, Order, OrderItem, ProductReview, Wishlist
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize RESTful API
api = Api(app)
CORS(app)  # Enable CORS for frontend frameworks

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.get_total() for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        flash('Not enough stock available', 'danger')
        return redirect(url_for('home'))
    
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<int:cart_item_id>')
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Product removed from cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item.get_total() for item in cart_items)
    
    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total
    )
    db.session.add(order)
    
    # Create order items and update stock
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.product.stock:
            flash('Not enough stock available', 'danger')
            return redirect(url_for('cart'))
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
        
        # Update stock
        cart_item.product.stock -= cart_item.quantity
    
    # Clear cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    
    db.session.commit()
    flash('Order placed successfully!', 'success')
    return redirect(url_for('home'))

# Search route with filters
@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'name')
    
    products = Product.query
    
    if query:
        products = products.filter(Product.name.contains(query) | 
                                 Product.description.contains(query))
    
    if category:
        products = products.filter(Product.category == category)
    
    if min_price:
        products = products.filter(Product.price >= min_price)
    
    if max_price:
        products = products.filter(Product.price <= max_price)
    
    # Sort products
    if sort_by == 'price_asc':
        products = products.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        products = products.order_by(Product.price.desc())
    elif sort_by == 'name':
        products = products.order_by(Product.name.asc())
    
    products = products.all()
    
    return render_template('search_results.html', 
                         products=products, 
                         query=query, 
                         category=category,
                         min_price=min_price,
                         max_price=max_price,
                         sort_by=sort_by)

# Wishlist routes
@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Product already in wishlist'})
    
    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Added to wishlist'})

@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Removed from wishlist'})
    
    return jsonify({'success': False, 'message': 'Product not in wishlist'})

# Product review routes
@app.route('/add_review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if user already reviewed this product
    existing_review = ProductReview.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_review:
        flash('You have already reviewed this product', 'warning')
        return redirect(url_for('product_detail', product_id=product_id))
    
    rating = int(request.form.get('rating'))
    title = request.form.get('title', '')
    comment = request.form.get('comment', '')
    
    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5 stars', 'danger')
        return redirect(url_for('product_detail', product_id=product_id))
    
    review = ProductReview(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        title=title,
        comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

# Enhanced product detail route
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = ProductReview.query.filter_by(product_id=product_id).order_by(ProductReview.created_at.desc()).all()
    
    # Check if user has this in wishlist
    in_wishlist = False
    user_review = None
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first() is not None
        user_review = ProductReview.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    return render_template('product_detail.html', 
                         product=product, 
                         reviews=reviews,
                         in_wishlist=in_wishlist,
                         user_review=user_review)

# Update cart quantity
@app.route('/update_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    new_quantity = int(request.form.get('quantity', 1))
    
    if new_quantity <= 0:
        db.session.delete(cart_item)
    elif new_quantity > cart_item.product.stock:
        return jsonify({'success': False, 'message': 'Not enough stock'})
    else:
        cart_item.quantity = new_quantity
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Cart updated'})

# Search route with filters
class ProductListAPI(Resource):
    def get(self):
        products = Product.query.all()
        return [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'stock': p.stock,
            'image_url': p.image_url,
            'category': p.category
        } for p in products]

class ProductAPI(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'image_url': product.image_url,
            'category': product.category
        }

# Register API routes
api.add_resource(ProductListAPI, '/api/products')
api.add_resource(ProductAPI, '/api/products/<int:product_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)