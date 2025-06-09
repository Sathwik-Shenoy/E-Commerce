from app import app
from models import db, Product, User

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create sample products
        products = [
            Product(
                name='Smartphone X',
                description='Latest smartphone with advanced features',
                price=999.99,
                stock=10,
                image_url='https://via.placeholder.com/300',
                category='Electronics'
            ),
            Product(
                name='Laptop Pro',
                description='High-performance laptop for professionals',
                price=1499.99,
                stock=5,
                image_url='https://via.placeholder.com/300',
                category='Electronics'
            ),
            Product(
                name='Running Shoes',
                description='Comfortable running shoes for athletes',
                price=79.99,
                stock=20,
                image_url='https://via.placeholder.com/300',
                category='Sports'
            ),
            Product(
                name='Coffee Maker',
                description='Automatic coffee maker with timer',
                price=49.99,
                stock=15,
                image_url='https://via.placeholder.com/300',
                category='Home'
            )
        ]
        
        # Add products to database
        for product in products:
            db.session.add(product)
        
        # Create a sample user
        user = User(username='demo', email='demo@example.com')
        user.set_password('password123')
        db.session.add(user)
        
        # Commit all changes
        db.session.commit()
        print('Database initialized with sample data!')

if __name__ == '__main__':
    init_db() 