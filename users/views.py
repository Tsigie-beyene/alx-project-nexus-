from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer

class RegisterView(APIView):
    """
    User registration endpoint.
    
    Allows new users to create accounts with username, email, and password.
    The password is automatically hashed and the user is created in the system.
    """
    permission_classes = [AllowAny]  # Allow anyone to register
    
    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Unique username for the account",
                    example="john_doe"
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description="Valid email address",
                    example="john@example.com"
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Secure password (minimum 8 characters)",
                    example="securepassword123"
                ),
            }
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="User created successfully"
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request - Invalid data or user already exists",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            example=["This field is required."]
                        ),
                        'email': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            example=["Enter a valid email address."]
                        ),
                        'password': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            example=["This field is required."]
                        )
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    User profile endpoint.
    
    Allows authenticated users to retrieve their profile information.
    Requires valid JWT authentication token.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get current user's profile information",
        responses={
            200: openapi.Response(
                description="User profile retrieved successfully",
                schema=UserSerializer
            ),
            401: "Unauthorized - Valid authentication token required"
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)