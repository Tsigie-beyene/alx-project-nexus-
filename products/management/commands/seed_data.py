from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='Number of categories to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=20,
            help='Number of products to create per category'
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed data...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and gardening'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
            {'name': 'Toys & Games', 'description': 'Toys and entertainment'},
            {'name': 'Health & Beauty', 'description': 'Health and beauty products'},
            {'name': 'Automotive', 'description': 'Automotive parts and accessories'},
        ]
        
        categories = []
        for i, cat_data in enumerate(categories_data[:options['categories']]):
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # Sample product data
        product_templates = [
            # Electronics
            [
                {'name': 'Gaming Laptop', 'description': 'High-performance gaming laptop with RGB keyboard', 'price': 1299.99, 'weight': 2.5},
                {'name': 'Wireless Headphones', 'description': 'Noise-cancelling wireless headphones', 'price': 199.99, 'weight': 0.3},
                {'name': 'Smartphone', 'description': 'Latest smartphone with advanced camera', 'price': 899.99, 'weight': 0.2},
                {'name': 'Tablet', 'description': '10-inch tablet for work and entertainment', 'price': 399.99, 'weight': 0.5},
                {'name': 'Smart Watch', 'description': 'Fitness tracking smartwatch', 'price': 299.99, 'weight': 0.1},
            ],
            # Clothing
            [
                {'name': 'Cotton T-Shirt', 'description': 'Comfortable cotton t-shirt', 'price': 19.99, 'weight': 0.2},
                {'name': 'Denim Jeans', 'description': 'Classic blue denim jeans', 'price': 49.99, 'weight': 0.5},
                {'name': 'Winter Jacket', 'description': 'Warm winter jacket', 'price': 89.99, 'weight': 1.2},
                {'name': 'Running Shoes', 'description': 'Lightweight running shoes', 'price': 79.99, 'weight': 0.8},
                {'name': 'Dress Shirt', 'description': 'Formal dress shirt', 'price': 39.99, 'weight': 0.3},
            ],
            # Books
            [
                {'name': 'Programming Python', 'description': 'Learn Python programming', 'price': 29.99, 'weight': 0.8},
                {'name': 'Fiction Novel', 'description': 'Bestselling fiction novel', 'price': 14.99, 'weight': 0.5},
                {'name': 'Cookbook', 'description': 'Collection of delicious recipes', 'price': 24.99, 'weight': 1.0},
                {'name': 'History Book', 'description': 'Comprehensive history guide', 'price': 19.99, 'weight': 0.7},
                {'name': 'Science Magazine', 'description': 'Monthly science magazine', 'price': 9.99, 'weight': 0.3},
            ],
            # Home & Garden
            [
                {'name': 'Garden Tool Set', 'description': 'Complete garden tool set', 'price': 59.99, 'weight': 2.0},
                {'name': 'Kitchen Blender', 'description': 'High-speed kitchen blender', 'price': 79.99, 'weight': 1.5},
                {'name': 'LED Light Bulbs', 'description': 'Energy-efficient LED bulbs pack', 'price': 19.99, 'weight': 0.3},
                {'name': 'Coffee Maker', 'description': 'Automatic coffee maker', 'price': 89.99, 'weight': 2.2},
                {'name': 'Plant Pot Set', 'description': 'Decorative plant pots', 'price': 34.99, 'weight': 1.0},
            ],
            # Sports
            [
                {'name': 'Basketball', 'description': 'Official size basketball', 'price': 29.99, 'weight': 0.6},
                {'name': 'Yoga Mat', 'description': 'Non-slip yoga mat', 'price': 24.99, 'weight': 0.8},
                {'name': 'Dumbbells Set', 'description': 'Adjustable dumbbells', 'price': 149.99, 'weight': 5.0},
                {'name': 'Tennis Racket', 'description': 'Professional tennis racket', 'price': 89.99, 'weight': 0.3},
                {'name': 'Cycling Helmet', 'description': 'Safety cycling helmet', 'price': 39.99, 'weight': 0.4},
            ],
        ]

        # Create products
        products_created = 0
        for i, category in enumerate(categories):
            if i < len(product_templates):
                templates = product_templates[i]
            else:
                # Generate generic products for additional categories
                templates = [
                    {'name': f'Product {j+1}', 'description': f'Generic product {j+1}', 'price': random.uniform(10, 100), 'weight': random.uniform(0.1, 2.0)}
                    for j in range(5)
                ]
            
            for j, template in enumerate(templates[:options['products']]):
                # Add some variation
                price_variation = random.uniform(0.8, 1.2)
                price = Decimal(str(round(template['price'] * price_variation, 2)))
                
                # Randomly add sale prices
                sale_price = None
                if random.random() < 0.3:  # 30% chance of being on sale
                    discount_factor = Decimal(str(random.uniform(0.6, 0.9)))
                    sale_price = price * discount_factor
                    sale_price = Decimal(str(round(sale_price, 2)))
                
                product, created = Product.objects.get_or_create(
                    name=template['name'],
                    category=category,
                    defaults={
                        'description': template['description'],
                        'price': price,
                        'sale_price': sale_price,
                        'stock': random.randint(0, 50),
                        'status': random.choice(['active', 'active', 'active', 'draft']),  # Mostly active
                        'is_featured': random.random() < 0.2,  # 20% chance of being featured
                        'weight': template.get('weight', random.uniform(0.1, 2.0)),
                        'dimensions': f"{random.randint(10, 50)}x{random.randint(10, 50)}x{random.randint(5, 20)}cm"
                    }
                )
                
                if created:
                    products_created += 1
                    if products_created % 10 == 0:
                        self.stdout.write(f'Created {products_created} products...')

        # Create a superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('Created superuser: admin/admin123')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded data! Created {len(categories)} categories and {products_created} products.'
            )
        ) 