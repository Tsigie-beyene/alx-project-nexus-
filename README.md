# E-Commerce API Backend

A robust RESTful API backend for an e-commerce product catalog built with Django and Django REST Framework.

## 🚀 Features

- **RESTful API** with comprehensive CRUD operations
- **JWT Authentication** for secure user management
- **Product & Category Management** with filtering and search
- **User Management** with registration and authentication
- **Swagger/OpenAPI Documentation** for easy API exploration
- **Database Optimization** with proper indexing
- **Environment Configuration** for secure deployment
- **Django Debug Toolbar** for development debugging

## 🛠️ Tech Stack

- **Backend**: Django 5.2.4
- **API Framework**: Django REST Framework 3.16.0
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **Filtering**: django-filter
- **Environment**: python-dotenv

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
Copy the example configuration file:
```bash
cp config.env.example config.env
```

Edit `config.env` with your database credentials:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 5. Database Setup
```bash
cd ecommerce_backend
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/
```

### API Information
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

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...."
}
```

### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
    "access": "new_access_token_here"
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

**Response:**
```json
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/products/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Gaming Laptop",
            "description": "High-performance gaming laptop",
            "price": "1299.99",
            "stock": 5,
            "category": {
                "id": 1,
                "name": "Electronics",
                "description": "Electronic devices and gadgets"
            },
            "category_id": 1,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

### Get Single Product
```http
GET /api/products/products/{id}/
```

### Create Product
```http
POST /api/products/products/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "name": "New Product",
    "description": "Product description",
    "price": "99.99",
    "stock": 10,
    "category_id": 1
}
```

### Update Product
```http
PUT /api/products/products/{id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "name": "Updated Product Name",
    "description": "Updated description",
    "price": "89.99",
    "stock": 15,
    "category_id": 1
}
```

### Delete Product
```http
DELETE /api/products/products/{id}/
Authorization: Bearer your_access_token
```

## 📂 Categories API

### List Categories
```http
GET /api/products/categories/
```

**Query Parameters:**
- `search`: Search in name and description
- `ordering`: Sort by field (name, id)

### Get Single Category
```http
GET /api/products/categories/{id}/
```

### Create Category
```http
POST /api/products/categories/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "name": "New Category",
    "description": "Category description"
}
```

### Update Category
```http
PUT /api/products/categories/{id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "name": "Updated Category",
    "description": "Updated description"
}
```

### Delete Category
```http
DELETE /api/products/categories/{id}/
Authorization: Bearer your_access_token
```

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
```http
GET /api/users/profile/
Authorization: Bearer your_access_token
```

### Update Profile
```http
PUT /api/users/profile/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "username": "updated_username",
    "email": "updated@example.com"
}
```

## 🔍 Filtering and Search

### Product Filtering Examples

**Filter by Category:**
```http
GET /api/products/products/?category=1
```

**Search Products:**
```http
GET /api/products/products/?search=laptop
```

**Filter by Stock:**
```http
GET /api/products/products/?stock=5
```

**Sort by Price (High to Low):**
```http
GET /api/products/products/?ordering=-price
```

**Sort by Creation Date (Newest First):**
```http
GET /api/products/products/?ordering=-created_at
```

**Combined Filters:**
```http
GET /api/products/products/?category=1&search=laptop&ordering=-price&page=2
```

### Category Filtering Examples

**Search Categories:**
```http
GET /api/products/categories/?search=electronics
```

**Sort Categories:**
```http
GET /api/products/categories/?ordering=name
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

**Custom Page:**
```http
GET /api/products/products/?page=2
```

## 🛡️ Error Handling

The API returns appropriate HTTP status codes and error messages:

### Common Error Responses

**400 Bad Request:**
```json
{
    "field_name": ["Error message for this field"]
}
```

**401 Unauthorized:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
    "detail": "Not found."
}
```

**500 Internal Server Error:**
```json
{
    "detail": "Internal server error."
}
```

## 🧪 Testing the API

### Using curl

**Get API Info:**
```bash
curl http://127.0.0.1:8000/
```

**Get Access Token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**List Products:**
```bash
curl http://127.0.0.1:8000/api/products/products/
```

**Create Product (with authentication):**
```bash
curl -X POST http://127.0.0.1:8000/api/products/products/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "Test description",
    "price": "29.99",
    "stock": 5,
    "category_id": 1
  }'
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

# Create a product
new_product = requests.post(f"{base_url}/api/products/products/", 
    headers=headers,
    json={
        "name": "New Product",
        "description": "Description",
        "price": "99.99",
        "stock": 10,
        "category_id": 1
    }
)
print(new_product.json())
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

### Debug Toolbar
The Django Debug Toolbar is automatically enabled in development mode and provides:
- Database query monitoring
- Performance profiling
- Template debugging
- Request/response analysis

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in your environment variables
2. Configure a production database
3. Set up proper `ALLOWED_HOSTS`
4. Use a production WSGI server (Gunicorn, uWSGI)
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

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/swagger/`
- Review the Django admin panel at `/admin/`

---

**Happy Coding! 🚀** 
