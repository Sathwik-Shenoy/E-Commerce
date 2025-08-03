#!/usr/bin/env python3
"""
Sample data initialization script for E-commerce application
Run this script to populate the database with sample data
"""

from app import app
from models import db, User, Product, Category, ProductImage, ProductReview
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for the e-commerce application"""
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Clear existing data
        db.session.query(ProductReview).delete()
        db.session.query(ProductImage).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        
        # Create sample users
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'sarah_jones', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Jones'},
        ]
        
        users = []
        for user_data in users_data:
            user = User(**user_data)
            user.set_password('password123')
            db.session.add(user)
            users.append(user)
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Latest electronic gadgets and devices'},
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Trendy fashion and apparel'},
            {'name': 'Books', 'slug': 'books', 'description': 'Books, magazines, and literature'},
            {'name': 'Home & Living', 'slug': 'home-living', 'description': 'Home decor and living essentials'},
            {'name': 'Sports & Fitness', 'slug': 'sports-fitness', 'description': 'Sports equipment and fitness gear'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
            categories.append(category)
        
        db.session.commit()
        
        # Create sample products
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.',
                'price': 199.99,
                'stock': 25,
                'category': 'Electronics',
                'category_id': categories[0].id,
                'brand': 'SoundMax',
                'sku': 'SM-WH-001',
                'weight': 0.3,
                'dimensions': '20x18x8 cm',
                'is_featured': True,
                'discount_percentage': 15,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
            },
            {
                'name': 'Smartphone 128GB',
                'description': 'Latest smartphone with advanced camera system, fast processor, and all-day battery life.',
                'price': 699.99,
                'stock': 15,
                'category': 'Electronics',
                'category_id': categories[0].id,
                'brand': 'TechPhone',
                'sku': 'TP-SP-128',
                'weight': 0.18,
                'dimensions': '15x7x0.8 cm',
                'is_featured': True,
                'discount_percentage': 10,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500',
            },
            {
                'name': 'Laptop 15.6" Intel i7',
                'description': 'Powerful laptop with Intel i7 processor, 16GB RAM, and 512GB SSD. Perfect for work and gaming.',
                'price': 1299.99,
                'stock': 8,
                'category': 'Electronics',
                'category_id': categories[0].id,
                'brand': 'CompuTech',
                'sku': 'CT-LP-I7',
                'weight': 2.1,
                'dimensions': '36x25x2 cm',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500',
            },
            
            # Clothing
            {
                'name': 'Premium Cotton T-Shirt',
                'description': 'Comfortable and stylish cotton t-shirt available in multiple colors. Made from 100% organic cotton.',
                'price': 29.99,
                'stock': 50,
                'category': 'Clothing',
                'category_id': categories[1].id,
                'brand': 'StyleWear',
                'sku': 'SW-TS-001',
                'weight': 0.2,
                'dimensions': 'Medium',
                'discount_percentage': 20,
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500',
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic blue denim jeans with a modern fit. Durable and comfortable for everyday wear.',
                'price': 79.99,
                'stock': 30,
                'category': 'Clothing',
                'category_id': categories[1].id,
                'brand': 'DenimCo',
                'sku': 'DC-DJ-001',
                'weight': 0.6,
                'dimensions': '32x34 inches',
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500',
            },
            
            # Books
            {
                'name': 'The Art of Programming',
                'description': 'Comprehensive guide to modern programming techniques and best practices. Perfect for developers.',
                'price': 49.99,
                'stock': 20,
                'category': 'Books',
                'category_id': categories[2].id,
                'brand': 'TechBooks',
                'sku': 'TB-AP-001',
                'weight': 0.8,
                'dimensions': '24x17x3 cm',
                'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500',
            },
            {
                'name': 'Mystery Novel Collection',
                'description': 'Collection of thrilling mystery novels by bestselling authors. Hours of suspenseful reading.',
                'price': 34.99,
                'stock': 35,
                'category': 'Books',
                'category_id': categories[2].id,
                'brand': 'Mystery Press',
                'sku': 'MP-MN-COL',
                'weight': 1.2,
                'dimensions': '20x13x4 cm',
                'discount_percentage': 25,
                'image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500',
            },
            
            # Home & Living
            {
                'name': 'Ceramic Coffee Mug Set',
                'description': 'Beautiful set of 4 ceramic coffee mugs with elegant design. Perfect for your morning coffee.',
                'price': 39.99,
                'stock': 40,
                'category': 'Home',
                'category_id': categories[3].id,
                'brand': 'HomeStyle',
                'sku': 'HS-CM-SET4',
                'weight': 1.5,
                'dimensions': '12x9x10 cm each',
                'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=500',
            },
            {
                'name': 'Decorative Table Lamp',
                'description': 'Modern decorative table lamp with adjustable brightness. Adds warmth to any room.',
                'price': 89.99,
                'stock': 12,
                'category': 'Home',
                'category_id': categories[3].id,
                'brand': 'LightCraft',
                'sku': 'LC-TL-001',
                'weight': 2.3,
                'dimensions': '15x15x35 cm',
                'is_featured': True,
                'discount_percentage': 30,
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500',
            },
            
            # Sports & Fitness
            {
                'name': 'Yoga Mat Premium',
                'description': 'High-quality yoga mat with excellent grip and cushioning. Perfect for yoga and fitness exercises.',
                'price': 59.99,
                'stock': 25,
                'category': 'Sports',
                'category_id': categories[4].id,
                'brand': 'FitGear',
                'sku': 'FG-YM-PREM',
                'weight': 1.8,
                'dimensions': '183x61x0.6 cm',
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=500',
            },
            {
                'name': 'Resistance Bands Set',
                'description': 'Complete set of resistance bands for strength training and rehabilitation. Includes different resistance levels.',
                'price': 24.99,
                'stock': 45,
                'category': 'Sports',
                'category_id': categories[4].id,
                'brand': 'FlexFit',
                'sku': 'FF-RB-SET',
                'weight': 0.5,
                'dimensions': 'Various sizes',
                'discount_percentage': 35,
                'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500',
            },
        ]
        
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)
            products.append(product)
        
        db.session.commit()
        
        # Create sample reviews
        review_comments = [
            "Great product! Exactly what I was looking for.",
            "Excellent quality and fast shipping. Highly recommended!",
            "Good value for money. Would buy again.",
            "Perfect! Meets all my expectations.",
            "Outstanding product quality. Very satisfied with my purchase.",
            "Amazing! Better than I expected.",
            "Solid product with great features.",
            "Love it! Will definitely recommend to friends.",
            "Fantastic quality and design.",
            "Exactly as described. Very happy with this purchase.",
        ]
        
        review_titles = [
            "Excellent Purchase!",
            "Highly Recommended",
            "Great Quality",
            "Perfect Product",
            "Amazing Value",
            "Love It!",
            "Outstanding",
            "Fantastic",
            "Exactly What I Needed",
            "Best Purchase Ever",
        ]
        
        # Add reviews for some products
        for product in random.sample(products, 8):
            num_reviews = random.randint(1, 4)
            for _ in range(num_reviews):
                user = random.choice(users)
                # Avoid duplicate reviews from same user
                existing_review = ProductReview.query.filter_by(user_id=user.id, product_id=product.id).first()
                if not existing_review:
                    review = ProductReview(
                        user_id=user.id,
                        product_id=product.id,
                        rating=random.randint(3, 5),  # Good ratings only
                        title=random.choice(review_titles),
                        comment=random.choice(review_comments),
                        is_verified=random.choice([True, False]),
                        helpful_count=random.randint(0, 10),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 90))
                    )
                    db.session.add(review)
        
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print(f"📊 Created:")
        print(f"   - {len(users)} users")
        print(f"   - {len(categories)} categories")
        print(f"   - {len(products)} products")
        print(f"   - {ProductReview.query.count()} reviews")
        print("\n🔐 Sample user credentials:")
        print("   Username: john_doe, Password: password123")
        print("   Username: jane_smith, Password: password123")
        print("   (and so on for other users)")

if __name__ == '__main__':
    create_sample_data()
