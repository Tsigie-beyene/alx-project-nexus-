from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="🛍️ E-Commerce API",
        default_version='v1',
        description="""
        # E-Commerce API Documentation
        
        A comprehensive RESTful API for e-commerce operations including product management, user authentication, and more.
        
        ## Features
        - 🔐 **JWT Authentication** - Secure token-based authentication
        - 📦 **Product Management** - Full CRUD operations for products
        - 🏷️ **Category Management** - Organize products by categories
        - 👤 **User Management** - User registration and profile management
        - 🔍 **Advanced Filtering** - Filter and sort products
        - 📝 **Interactive Documentation** - Test endpoints directly from the docs
        
        ## Getting Started
        1. **Register a user** using `/api/users/register/`
        2. **Get authentication token** using `/api/token/`
        3. **Use the token** in the Authorization header: `Bearer <your_token>`
        4. **Explore the API** using the endpoints below
        
        ## Authentication
        This API uses JWT (JSON Web Tokens) for authentication. Include your token in the Authorization header:
        ```
        Authorization: Bearer <your_access_token>
        ```
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            email="your_email@example.com",
            name="API Support",
            url="https://github.com/yourusername/ecommerce-api"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
    ),
    public=True,
    permission_classes=[],
    # IMPORTANT: Patterns here must mirror the actual URL prefixes below.
    # Otherwise, Swagger will generate incorrect paths and "Try it out"
    # will call non-existent endpoints.
    patterns=[
        path('api/products/', include('products.urls')),
        path('api/users/', include('users.urls')),
    ],
)

def api_info(request):
    """API information endpoint"""
    return JsonResponse({
        'message': 'Welcome to E-Commerce API',
        'version': 'v1',
        'description': 'A comprehensive RESTful API for e-commerce operations',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/swagger/',
            'redoc_docs': '/redoc/',
            'products': '/api/products/',
            'users': '/api/users/',
            'token': '/api/token/',
            'token_refresh': '/api/token/refresh/',
        },
        'documentation': {
            'swagger_ui': '/swagger/',
            'redoc': '/redoc/',
        }
    })

urlpatterns = [
    # Beautiful landing page
    path('', TemplateView.as_view(template_name='api_landing.html'), name='landing'),
    
    # API info endpoint (accessible at /api/info/)
    path('api/info/', api_info, name='api_info'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API endpoints
    path('api/products/', include('products.urls')),
    path('api/users/', include('users.urls')),
]

# Add Debug Toolbar URLs only in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]