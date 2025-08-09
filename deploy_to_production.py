#!/usr/bin/env python3
"""
Production Deployment Script for ALX Project Nexus
This script automates the deployment process for the E-Commerce API Backend.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    print(f"🚀 Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_git_status():
    """Check if git repository is clean."""
    print("🔍 Checking Git status...")
    result = run_command('git status --porcelain', check=False)
    if result.stdout.strip():
        print("⚠️  Uncommitted changes detected. Committing changes...")
        run_command('git add .')
        run_command('git commit -m "Production deployment preparation"')
    else:
        print("✅ Git repository is clean")

def install_production_dependencies():
    """Install production dependencies."""
    print("📦 Installing production dependencies...")
    run_command('pip install gunicorn whitenoise')

def collect_static_files():
    """Collect static files for production."""
    print("📁 Collecting static files...")
    run_command('python manage.py collectstatic --noinput')

def run_migrations():
    """Run database migrations."""
    print("🗄️  Running migrations...")
    run_command('python manage.py migrate')

def create_superuser_if_needed():
    """Create superuser if it doesn't exist."""
    print("👤 Checking superuser...")
    try:
        result = run_command('python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).count())"', check=False)
        if result.stdout.strip() == '0':
            print("⚠️  No superuser found. Creating one...")
            run_command('python manage.py createsuperuser --noinput --username admin --email admin@example.com', check=False)
        else:
            print("✅ Superuser already exists")
    except:
        print("⚠️  Could not check superuser status")

def test_application():
    """Test the application."""
    print("🧪 Testing application...")
    run_command('python manage.py check --deploy')

def create_production_config():
    """Create production configuration."""
    print("⚙️  Creating production configuration...")
    
    # Create production config.env
    production_config = """# Production Settings
SECRET_KEY=django-insecure-production-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=your-app-name.herokuapp.com,localhost,127.0.0.1

# Database Settings (PostgreSQL for production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_production_db_name
DB_USER=your_production_db_user
DB_PASSWORD=your_production_db_password
DB_HOST=your_production_db_host
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Security Settings
SECURE_SSL_REDIRECT=True
"""
    
    with open('config.env.production', 'w') as f:
        f.write(production_config)
    
    print("✅ Production configuration created")

def main():
    """Main deployment function."""
    print("🚀 Starting Production Deployment for ALX Project Nexus")
    print("=" * 60)
    
    # Check prerequisites
    check_git_status()
    
    # Install dependencies
    install_production_dependencies()
    
    # Run Django setup
    run_migrations()
    collect_static_files()
    create_superuser_if_needed()
    
    # Test application
    test_application()
    
    # Create production config
    create_production_config()
    
    print("\n🎉 Production deployment preparation completed!")
    print("\n📋 Next steps for deployment:")
    print("1. Choose your deployment platform:")
    print("   - Heroku: heroku create && git push heroku main")
    print("   - Railway: railway login && railway up")
    print("   - Render: Connect your GitHub repository")
    print("   - DigitalOcean: Connect your GitHub repository")
    print("\n2. Set environment variables in your deployment platform")
    print("3. Configure your database (PostgreSQL recommended)")
    print("4. Set up custom domain (optional)")
    print("\n📚 Documentation:")
    print("- API Documentation: https://your-app-url.com/swagger/")
    print("- Admin Panel: https://your-app-url.com/admin/")
    print("- API Info: https://your-app-url.com/api/info/")

if __name__ == "__main__":
    main()
