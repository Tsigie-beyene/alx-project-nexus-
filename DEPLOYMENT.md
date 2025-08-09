# 🚀 Deployment Guide

This guide will help you deploy the E-Commerce API Backend on your local machine or production server.

## 📋 Prerequisites

### Required Software
1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL 12+** - [Download PostgreSQL](https://www.postgresql.org/download/)
3. **Git** - [Download Git](https://git-scm.com/downloads)

### System Requirements
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: 1GB free space
- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+

## 🔧 Step-by-Step Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/Tsigie-beyene/alx-project-nexus-
cd alx-project-nexus-
```

### 2. Set Up Python Environment

#### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL

#### Install PostgreSQL

**Windows:**
1. Download from [PostgreSQL website](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Set a password for the `postgres` user
4. Add PostgreSQL to your PATH

**macOS:**
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ecommerce_backend_db;

# Create user (optional)
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_backend_db TO ecommerce_user;

# Exit PostgreSQL
\q
```

### 4. Configure Environment Variables

1. **Copy the example configuration:**
```bash
cp config.env.example config.env  # if exists
```

2. **Edit `config.env` with your database credentials:**
```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_backend_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Security Settings
SECURE_SSL_REDIRECT=False
```

### 5. Run Django Setup

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Main API**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/swagger/

## 🐳 Docker Deployment (Alternative)

### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ecommerce_backend_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_NAME=ecommerce_backend_db
      - DB_USER=postgres
      - DB_PASSWORD=your_password

volumes:
  postgres_data:
```

### 3. Run with Docker
```bash
# Build and start services
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 🔒 Production Deployment

### 1. Security Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Set up HTTPS/SSL
- [ ] Use environment variables for sensitive data
- [ ] Configure proper database credentials
- [ ] Set up logging
- [ ] Configure static file serving

### 2. Production Settings
Update `config.env` for production:
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
SECURE_SSL_REDIRECT=True
```

### 3. Using Gunicorn (Production WSGI Server)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 ecommerce_backend.wsgi:application
```

### 4. Using Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🧪 Testing the Deployment

### 1. API Endpoints Test
```bash
# Test the main endpoint
curl http://127.0.0.1:8000/

# Test API documentation
curl http://127.0.0.1:8000/swagger/

# Test products endpoint
curl http://127.0.0.1:8000/api/products/products/
```

### 2. Database Connection Test
```bash
# Test database connection
python manage.py dbshell
```

### 3. Static Files Test
```bash
# Check if static files are collected
ls staticfiles/
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check if PostgreSQL is running
   - Verify database credentials in `config.env`
   - Ensure database exists

2. **Port Already in Use**
   - Change port: `python manage.py runserver 8001`
   - Kill existing process: `lsof -ti:8000 | xargs kill -9`

3. **Permission Denied**
   - Check file permissions
   - Run with appropriate user privileges

4. **Module Not Found**
   - Activate virtual environment
   - Install missing dependencies: `pip install -r requirements.txt`

### Logs
Check logs in the `logs/` directory:
```bash
tail -f logs/django.log
```

## 📞 Support

If you encounter issues:
1. Check the [README.md](README.md) for detailed documentation
2. Review the API documentation at `/swagger/`
3. Check the logs in `logs/django.log`
4. Create an issue in the repository

## 🎯 Next Steps

After successful deployment:
1. **Explore the API**: Visit http://127.0.0.1:8000/swagger/
2. **Create test data**: Use the admin panel or API endpoints
3. **Set up monitoring**: Configure logging and monitoring
4. **Backup strategy**: Set up database backups
5. **Security audit**: Review security settings
6. **Performance optimization**: Monitor and optimize performance

---

**Happy Deploying! 🚀**
