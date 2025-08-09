# 🚀 Production Deployment Guide

## 📋 **Current Status**
✅ **Development deployment completed successfully**
- Server running on: http://127.0.0.1:8000/
- Database: SQLite (development)
- Environment: Development mode

## 🎯 **Production Deployment Options**

### Option 1: **Heroku Deployment** (Recommended for beginners)

#### Prerequisites
1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your project is in a Git repository

#### Steps
```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create your-app-name

# 3. Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# 4. Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# 5. Deploy
git add .
git commit -m "Production deployment"
git push heroku main

# 6. Run migrations
heroku run python manage.py migrate

# 7. Create superuser
heroku run python manage.py createsuperuser

# 8. Collect static files
heroku run python manage.py collectstatic --noinput
```

### Option 2: **DigitalOcean App Platform**

#### Steps
1. **Create DigitalOcean Account**: Sign up at [digitalocean.com](https://digitalocean.com)
2. **Connect Repository**: Connect your GitHub repository
3. **Configure App**: Set environment variables and build commands
4. **Deploy**: Click deploy and wait for completion

### Option 3: **AWS EC2 Deployment**

#### Prerequisites
1. **AWS Account**: Sign up at [aws.amazon.com](https://aws.amazon.com)
2. **EC2 Instance**: Launch Ubuntu 20.04 LTS instance
3. **Domain Name**: (Optional) for custom domain

#### Steps
```bash
# 1. Connect to EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Update system
sudo apt update && sudo apt upgrade -y

# 3. Install dependencies
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y

# 4. Clone repository
git clone https://github.com/Tsigie-beyene/alx-project-nexus-.git
cd alx-project-nexus-

# 5. Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Configure PostgreSQL
sudo -u postgres psql
CREATE DATABASE ecommerce_backend_db;
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_backend_db TO ecommerce_user;
\q

# 7. Configure environment variables
cp config.env.example config.env
# Edit config.env with production settings

# 8. Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# 9. Set up Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 ecommerce_backend.wsgi:application

# 10. Configure Nginx
sudo nano /etc/nginx/sites-available/ecommerce
# Add nginx configuration

# 11. Enable site
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 4: **Docker Deployment**

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce_backend.wsgi:application"]
```

#### Create docker-compose.yml
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
    command: gunicorn --bind 0.0.0.0:8000 ecommerce_backend.wsgi:application
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
      - DEBUG=False
      - SECRET_KEY=your-production-secret-key

volumes:
  postgres_data:
```

## 🔒 **Production Security Checklist**

### Environment Variables
```env
# Production Settings
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-app-name.herokuapp.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=production_db_name
DB_USER=production_db_user
DB_PASSWORD=production_db_password
DB_HOST=your-db-host
DB_PORT=5432
SECURE_SSL_REDIRECT=True
```

### Security Measures
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Use PostgreSQL database
- [ ] Configure proper logging
- [ ] Set up monitoring
- [ ] Configure backups

## 📊 **Performance Optimization**

### Database Optimization
```sql
-- Add indexes for better performance
CREATE INDEX idx_product_name ON products_product(name);
CREATE INDEX idx_product_category ON products_product(category_id);
CREATE INDEX idx_product_price ON products_product(price);
```

### Caching
```python
# Add Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 🧪 **Testing Production Deployment**

### Health Check
```bash
# Test main endpoint
curl https://your-domain.com/

# Test API endpoints
curl https://your-domain.com/api/info/
curl https://your-domain.com/api/products/products/
```

### Performance Testing
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test performance
ab -n 1000 -c 10 https://your-domain.com/
```

## 📞 **Support**

If you encounter issues during production deployment:

1. **Check Logs**: Review application and server logs
2. **Monitor Performance**: Use tools like New Relic or DataDog
3. **Backup Strategy**: Set up automated backups
4. **SSL Certificate**: Ensure HTTPS is properly configured

## 🎯 **Recommended Next Steps**

1. **Choose Deployment Platform**: Select Heroku, DigitalOcean, AWS, or Docker
2. **Set Up Domain**: Configure custom domain (optional)
3. **Configure SSL**: Set up HTTPS certificate
4. **Set Up Monitoring**: Implement application monitoring
5. **Configure Backups**: Set up automated database backups
6. **Performance Testing**: Test under load
7. **Security Audit**: Review security settings

---

**Your application is ready for production deployment! 🚀**
