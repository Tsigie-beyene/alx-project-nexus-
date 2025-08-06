from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model with enhanced validation.
    """
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
        read_only_fields = ['id', 'product_count']
    
    def get_product_count(self, obj):
        """Get the number of products in this category."""
        return obj.products.count()
    
    def validate_name(self, value):
        """Validate category name uniqueness."""
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model with enhanced validation and nested category data.
    
    Features:
    - Nested category information for read operations
    - Category ID for write operations
    - Price and stock validation
    - Optimized queries
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True,
        error_messages={'does_not_exist': 'Category with this ID does not exist.'}
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 
            'category', 'category_id', 'category_name', 'stock_status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'category_name', 'stock_status']
    
    def get_stock_status(self, obj):
        """Get human-readable stock status."""
        if obj.stock == 0:
            return "Out of Stock"
        elif obj.stock <= 5:
            return "Low Stock"
        else:
            return "In Stock"
    
    def validate_price(self, value):
        """Validate product price."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        if value > 999999.99:
            raise serializers.ValidationError("Price cannot exceed 999,999.99.")
        return value
    
    def validate_stock(self, value):
        """Validate product stock."""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        if value > 999999:
            raise serializers.ValidationError("Stock cannot exceed 999,999.")
        return value
    
    def validate_name(self, value):
        """Validate product name."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        return value.strip()
    
    def validate_description(self, value):
        """Validate product description."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Product description must be at least 10 characters long.")
        return value.strip()

class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product lists (optimized for performance).
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'category_name', 'stock_status']
    
    def get_stock_status(self, obj):
        """Get human-readable stock status."""
        if obj.stock == 0:
            return "Out of Stock"
        elif obj.stock <= 5:
            return "Low Stock"
        else:
            return "In Stock"