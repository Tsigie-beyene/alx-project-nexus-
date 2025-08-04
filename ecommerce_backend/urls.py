from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce API",
        default_version='v1',
        description="RESTful API for an e-commerce product catalog",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

def api_info(request):
    """API information endpoint"""
    return JsonResponse({
        'message': 'Welcome to E-Commerce API',
        'version': 'v1',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/swagger/',
            'products': '/api/products/',
            'users': '/api/users/',
            'token': '/api/token/',
            'token_refresh': '/api/token/refresh/',
        }
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/products/', include('products.urls')),
    path('api/users/', include('users.urls')),
]