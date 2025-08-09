# E-Commerce Backend - ProDev BE

A robust Django-based backend system for e-commerce product catalog management, designed for ALX Backend Engineering milestone.

## 🎯 Project Overview

This case study focuses on developing a robust backend system to support an e-commerce product catalog. The backend handles product data management, user authentication, and APIs for filtering, sorting, and pagination, simulating a real-world scenario for backend engineers.

## 🚀 Project Goals

- **CRUD APIs**: Build APIs for managing products, categories, and user authentication
- **Filtering, Sorting, Pagination**: Implement robust logic for efficient product discovery
- **Database Optimization**: Design a high-performance database schema to support seamless queries

## 🛠️ Technologies Used

- **Django**: For building a scalable backend framework
- **PostgreSQL**: As the relational database for optimized performance
- **JWT**: For secure user authentication
- **Swagger/OpenAPI**: To document and test APIs
- **Django REST Framework**: For building RESTful APIs
- **Django Filters**: For advanced filtering capabilities

## ✨ Key Features

### 1. CRUD Operations
- Create, read, update, and delete operations for products and categories
- User authentication and management features using JWT

### 2. API Features
- **Filtering and Sorting**: Allow users to filter products by category and sort by price
- **Pagination**: Implement paginated responses for large product datasets

### 3. API Documentation
- Use Swagger to generate API documentation
- Publish hosted API docs for easy frontend consumption

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Tsigie-beyene/alx-project-nexus-
cd alx-project-nexus-
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate   # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `config.env` file in the root directory:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_backend_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Seed Sample Data (Optional)
```bash
python manage.py seed_data
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/
```

### API Endpoints
- **Root Endpoint**: `GET /` - API information and available endpoints
- **Documentation**: `GET /swagger/` - Interactive API documentation
- **Admin Panel**: `GET /admin/` - Django admin interface

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Get Access Token
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Using Authentication
Include the access token in the Authorization header:
```http
Authorization: Bearer your_access_token_here
```

## 📦 Products API

### List Products
```http
GET /api/products/products/
```

**Query Parameters:**
- `search`: Search in name and description
- `category`: Filter by category ID
- `stock`: Filter by stock availability
- `ordering`: Sort by field (name, price, created_at, stock)
- `page`: Page number for pagination

**Example:**
```http
GET /api/products/products/?search=laptop&category=1&ordering=-price
```

### CRUD Operations
- `GET /api/products/products/` - List all products
- `POST /api/products/products/` - Create new product
- `GET /api/products/products/{id}/` - Get single product
- `PUT /api/products/products/{id}/` - Update product
- `DELETE /api/products/products/{id}/` - Delete product

## 📂 Categories API

### List Categories
```http
GET /api/products/categories/
```

**Query Parameters:**
- `search`: Search in name and description
- `ordering`: Sort by field (name, id)

### CRUD Operations
- `GET /api/products/categories/` - List all categories
- `POST /api/products/categories/` - Create new category
- `GET /api/products/categories/{id}/` - Get single category
- `PUT /api/products/categories/{id}/` - Update category
- `DELETE /api/products/categories/{id}/` - Delete category

## 👥 Users API

### User Registration
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123",
    "password2": "securepassword123"
}
```

### User Profile
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile

## 🔍 Filtering and Search Examples

### Product Filtering
```http
# Filter by Category
GET /api/products/products/?category=1

# Search Products
GET /api/products/products/?search=laptop

# Filter by Stock
GET /api/products/products/?stock=5

# Sort by Price (High to Low)
GET /api/products/products/?ordering=-price

# Combined Filters
GET /api/products/products/?category=1&search=laptop&ordering=-price&page=2
```

## 📄 Pagination

The API uses page-based pagination with a default page size of 10 items.

**Response Format:**
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/products/products/?page=2",
    "previous": null,
    "results": [...]
}
```

## 🧪 Testing the API

### Using curl
```bash
# Get API Info
curl http://127.0.0.1:8000/

# Get Access Token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# List Products
curl http://127.0.0.1:8000/api/products/products/
```

### Using Python requests
```python
import requests

# Base URL
base_url = "http://127.0.0.1:8000"

# Get access token
auth_response = requests.post(f"{base_url}/api/token/", {
    "username": "your_username",
    "password": "your_password"
})
token = auth_response.json()["access"]

# Set up headers
headers = {"Authorization": f"Bearer {token}"}

# List products
products = requests.get(f"{base_url}/api/products/products/", headers=headers)
print(products.json())
```

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Django Shell
```bash
python manage.py shell
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in your environment variables
2. Configure a production database
3. Set up proper `ALLOWED_HOSTS`
4. Use a production WSGI server (Gunicorn)
5. Configure static file serving
6. Set up HTTPS

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=production_db_name
DB_USER=production_db_user
DB_PASSWORD=production_db_password
DB_HOST=your-db-host
DB_PORT=5432
```

## 📝 Git Commit Workflow

The project follows a structured commit workflow:
- `feat: set up Django project with PostgreSQL`
- `feat: implement user authentication with JWT`
- `feat: add product APIs with filtering and pagination`
- `feat: integrate Swagger documentation for API endpoints`
- `perf: optimize database queries with indexing`
- `docs: add API usage instructions in Swagger`

## 🎯 Evaluation Criteria

### 1. Functionality
- CRUD APIs for products, categories, and user authentication
- Filtering, sorting, and pagination logic implemented effectively

### 2. Code Quality
- Clean, maintainable, and well-documented code
- Proper database indexing for high-performance queries

### 3. User Experience
- API documentation is comprehensive and user-friendly
- Secure authentication implementation

### 4. Version Control
- Frequent and descriptive Git commit messages
- Well-organized repository structure

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/swagger/`
- Review the Django admin panel at `/admin/`

---

**Happy Coding! 🚀** 
