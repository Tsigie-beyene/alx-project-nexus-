from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryModelTest(TestCase):
    """Test cases for Category model."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic devices and gadgets"
        )
    
    def test_category_creation(self):
        """Test category creation."""
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.description, "Electronic devices and gadgets")
        self.assertEqual(str(self.category), "Electronics")
    
    def test_category_unique_name(self):
        """Test that category names are unique."""
        with self.assertRaises(Exception):
            Category.objects.create(
                name="Electronics",
                description="Another electronics category"
            )

class ProductModelTest(TestCase):
    """Test cases for Product model."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic devices"
        )
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone model",
            price=599.99,
            stock=50,
            category=self.category
        )
    
    def test_product_creation(self):
        """Test product creation."""
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.price, 599.99)
        self.assertEqual(self.product.stock, 50)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(str(self.product), "Smartphone")

class CategorySerializerTest(TestCase):
    """Test cases for CategorySerializer."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic devices"
        )
        self.serializer = CategorySerializer(instance=self.category)
    
    def test_contains_expected_fields(self):
        """Test that serializer contains expected fields."""
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'product_count'])
    
    def test_name_field_content(self):
        """Test name field content."""
        data = self.serializer.data
        self.assertEqual(data['name'], self.category.name)

class ProductSerializerTest(TestCase):
    """Test cases for ProductSerializer."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic devices"
        )
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone model",
            price=599.99,
            stock=50,
            category=self.category
        )
        self.serializer = ProductSerializer(instance=self.product)
    
    def test_contains_expected_fields(self):
        """Test that serializer contains expected fields."""
        data = self.serializer.data
        expected_fields = [
            'id', 'name', 'description', 'price', 'stock',
            'category', 'category_name', 'stock_status',
            'created_at', 'updated_at'
        ]
        self.assertCountEqual(data.keys(), expected_fields)
    
    def test_price_validation(self):
        """Test price validation."""
        invalid_data = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': -10.00,
            'stock': 10,
            'category_id': self.category.id
        }
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

class CategoryAPITest(APITestCase):
    """Test cases for Category API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category_data = {
            'name': 'Electronics',
            'description': 'Electronic devices and gadgets'
        }
    
    def test_create_category_authenticated(self):
        """Test creating category with authentication."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/products/categories/', self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Electronics')
    
    def test_create_category_unauthenticated(self):
        """Test creating category without authentication."""
        response = self.client.post('/api/products/categories/', self.category_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_categories(self):
        """Test listing categories."""
        Category.objects.create(name='Electronics', description='Electronic devices')
        response = self.client.get('/api/products/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class ProductAPITest(APITestCase):
    """Test cases for Product API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        self.product_data = {
            'name': 'Smartphone',
            'description': 'Latest smartphone model with advanced features',
            'price': 599.99,
            'stock': 50,
            'category_id': self.category.id
        }
    
    def test_create_product_authenticated(self):
        """Test creating product with authentication."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/products/products/', self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Smartphone')
    
    def test_list_products(self):
        """Test listing products."""
        Product.objects.create(
            name='Smartphone',
            description='Latest smartphone model',
            price=599.99,
            stock=50,
            category=self.category
        )
        response = self.client.get('/api/products/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_products_by_category(self):
        """Test filtering products by category."""
        Product.objects.create(
            name='Smartphone',
            description='Latest smartphone model',
            price=599.99,
            stock=50,
            category=self.category
        )
        response = self.client.get(f'/api/products/products/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_products(self):
        """Test searching products."""
        Product.objects.create(
            name='Smartphone',
            description='Latest smartphone model',
            price=599.99,
            stock=50,
            category=self.category
        )
        response = self.client.get('/api/products/products/?search=smartphone')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
