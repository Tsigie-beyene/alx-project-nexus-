from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    
    Provides CRUD operations for product categories with proper permissions.
    Only authenticated users can create, update, or delete categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="List all product categories",
        responses={
            200: openapi.Response(
                description="List of categories retrieved successfully",
                schema=CategorySerializer(many=True)
            ),
            401: "Unauthorized - Authentication required for write operations"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new product category",
        request_body=CategorySerializer,
        responses={
            201: openapi.Response(
                description="Category created successfully",
                schema=CategorySerializer
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    
    Provides CRUD operations for products with filtering, searching, and ordering capabilities.
    Features:
    - Filter by category
    - Search by name and description
    - Sort by price, name, or creation date
    - Optimized queries with select_related for category
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'stock']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'name', 'created_at', 'stock']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="List all products with filtering and search capabilities",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter products by category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search products by name, description, or category name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order results by: price, name, created_at, stock (prefix with - for descending)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of products retrieved successfully",
                schema=ProductSerializer(many=True)
            ),
            400: "Bad Request - Invalid filter parameters"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(
                description="Product created successfully",
                schema=ProductSerializer
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific product by ID",
        responses={
            200: openapi.Response(
                description="Product details retrieved successfully",
                schema=ProductSerializer
            ),
            404: "Not Found - Product does not exist"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)