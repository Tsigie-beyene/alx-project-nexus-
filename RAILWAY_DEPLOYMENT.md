# 🚀 Railway Deployment Guide for ALX Project Nexus

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Ensure your code is pushed to GitHub
3. **Railway CLI** (Optional): Install for local deployment

## 🎯 Step-by-Step Deployment

### Step 1: Connect to Railway

1. **Visit Railway Dashboard**
   - Go to [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `Tsigie-beyene/alx-project-nexus-`

### Step 2: Configure Environment Variables

1. **Go to Variables Tab**
   - Click on your project
   - Go to "Variables" tab

2. **Add Environment Variables**
```env
SECRET_KEY=django-insecure-production-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=your_railway_db_password
DB_HOST=your_railway_db_host
DB_PORT=5432
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
SECURE_SSL_REDIRECT=True
```

### Step 3: Add PostgreSQL Database

1. **Add PostgreSQL Service**
   - Click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically configure the database

2. **Connect Database to App**
   - Go back to your app service
   - Click "Connect" next to the PostgreSQL service
   - Railway will automatically set the database environment variables

### Step 4: Configure Build Settings

1. **Build Command**
   - Go to "Settings" tab
   - Set build command: `pip install -r requirements.txt`

2. **Start Command**
   - Set start command: `gunicorn ecommerce_backend.wsgi:application --bind 0.0.0.0:$PORT`

### Step 5: Deploy

1. **Automatic Deployment**
   - Railway will automatically deploy when you push to GitHub
   - Or click "Deploy" to trigger manual deployment

2. **Monitor Deployment**
   - Watch the deployment logs
   - Check for any errors

### Step 6: Run Migrations

1. **Access Railway CLI**
   - Install Railway CLI: `npm install -g @railway/cli`
   - Login: `railway login`

2. **Run Migrations**
```bash
railway run python manage.py migrate
```

3. **Create Superuser**
```bash
railway run python manage.py createsuperuser
```

4. **Collect Static Files**
```bash
railway run python manage.py collectstatic --noinput
```

## 🌐 Access Your Deployed Application

Once deployed, your application will be available at:
- **Main Application**: `https://your-app-name.railway.app/`
- **Admin Panel**: `https://your-app-name.railway.app/admin/`
- **API Documentation**: `https://your-app-name.railway.app/swagger/`
- **API Info**: `https://your-app-name.railway.app/api/info/`

## 🔧 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check the build logs in Railway dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **Database Connection Issues**
   - Check environment variables are correctly set
   - Ensure PostgreSQL service is connected
   - Verify database credentials

3. **Static Files Not Loading**
   - Run `railway run python manage.py collectstatic --noinput`
   - Check WhiteNoise configuration

4. **Migration Issues**
   - Run `railway run python manage.py migrate`
   - Check for any migration conflicts

## 📊 Monitoring

### Railway Dashboard
- **Logs**: View application logs in real-time
- **Metrics**: Monitor CPU, memory, and network usage
- **Deployments**: Track deployment history

### Application Health
- **Health Check**: `https://your-app-name.railway.app/api/info/`
- **Status Page**: Railway provides status page for your app

## 🔒 Security

### Environment Variables
- All sensitive data is stored in Railway environment variables
- Never commit secrets to your repository
- Use Railway's secure variable storage

### SSL/HTTPS
- Railway automatically provides SSL certificates
- All traffic is encrypted by default

## 📈 Scaling

### Automatic Scaling
- Railway automatically scales based on traffic
- No manual configuration required

### Performance Monitoring
- Monitor application performance in Railway dashboard
- Set up alerts for high resource usage

## 🎯 ALX Milestone Requirements

### ✅ Deployment Checklist

1. **✅ Production Deployment**
   - Application deployed to production platform
   - HTTPS enabled
   - Environment variables configured

2. **✅ Database Configuration**
   - PostgreSQL database configured
   - Migrations applied
   - Data integrity maintained

3. **✅ Performance Optimization**
   - Static files served efficiently
   - Database queries optimized
   - Application performance monitored

4. **✅ Security Measures**
   - Environment variables secured
   - HTTPS enabled
   - Security headers configured

## 🎉 Success!

Your E-Commerce API Backend is now successfully deployed to Railway and ready for your ALX milestone presentation!

### Next Steps
1. **Test Your Application**: Verify all endpoints work correctly
2. **Documentation**: Update your README with the live URL
3. **Presentation**: Prepare your demo for the ALX milestone review
4. **Monitoring**: Set up monitoring and alerts

---

**🚀 Congratulations on your successful deployment! 🎊**
