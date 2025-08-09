#!/usr/bin/env python3
"""
Deployment script for E-Commerce API Backend
This script automates the deployment process for the Django application.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def check_postgresql():
    """Check if PostgreSQL is installed and running."""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PostgreSQL detected")
            return True
        else:
            print("⚠️ PostgreSQL not found in PATH")
            return False
    except FileNotFoundError:
        print("⚠️ PostgreSQL not found in PATH")
        return False

def create_virtual_environment():
    """Create and activate virtual environment."""
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        run_command('python -m venv venv')
    else:
        print("✅ Virtual environment already exists")

def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    if platform.system() == "Windows":
        run_command('venv\\Scripts\\pip install -r requirements.txt')
    else:
        run_command('venv/bin/pip install -r requirements.txt')

def setup_database():
    """Setup PostgreSQL database."""
    print("Setting up database...")
    # This would need to be customized based on your PostgreSQL setup
    print("⚠️ Please ensure PostgreSQL is running and create the database manually:")
    print("   createdb ecommerce_backend_db")

def run_migrations():
    """Run Django migrations."""
    print("Running migrations...")
    if platform.system() == "Windows":
        run_command('venv\\Scripts\\python manage.py makemigrations')
        run_command('venv\\Scripts\\python manage.py migrate')
    else:
        run_command('venv/bin/python manage.py makemigrations')
        run_command('venv/bin/python manage.py migrate')

def create_superuser():
    """Create a superuser account."""
    print("Creating superuser...")
    print("⚠️ You will be prompted to enter superuser credentials")
    if platform.system() == "Windows":
        run_command('venv\\Scripts\\python manage.py createsuperuser', check=False)
    else:
        run_command('venv/bin/python manage.py createsuperuser', check=False)

def collect_static():
    """Collect static files."""
    print("Collecting static files...")
    if platform.system() == "Windows":
        run_command('venv\\Scripts\\python manage.py collectstatic --noinput')
    else:
        run_command('venv/bin/python manage.py collectstatic --noinput')

def main():
    """Main deployment function."""
    print("🚀 Starting E-Commerce API Backend Deployment")
    print("=" * 50)
    
    # Check prerequisites
    check_python_version()
    check_postgresql()
    
    # Setup environment
    create_virtual_environment()
    install_dependencies()
    
    # Setup database
    setup_database()
    
    # Run Django setup
    run_migrations()
    collect_static()
    create_superuser()
    
    print("\n🎉 Deployment completed successfully!")
    print("\nNext steps:")
    print("1. Update config.env with your database credentials")
    print("2. Start the development server: python manage.py runserver")
    print("3. Access the API at: http://127.0.0.1:8000/")
    print("4. Access admin panel at: http://127.0.0.1:8000/admin/")
    print("5. Access API docs at: http://127.0.0.1:8000/swagger/")

if __name__ == "__main__":
    main()
