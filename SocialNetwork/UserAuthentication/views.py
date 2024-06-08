from .models import User 
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny , IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserRegistrationSerializer , UserLoginSerializer, UserSerializer
from rest_framework import serializers

class UserRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    def create(self, request, *args, **kwargs):
            try:
                response = super().create(request, *args, **kwargs)
                response_data = {'message': 'User has been registered successfully'}
                response_data.update(response.data)
                return Response(response_data, status=response.status_code)
            except Exception as e:
                return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)            
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                
                user = User.objects.filter(email=email).first()
                if user and check_password(password, user.password):
                    access = AccessToken.for_user(user)
                    refresh = RefreshToken.for_user(user)
                    response_data = {
                        "message": f"User {user.username} has been logged in successfully!",
                        "refresh": str(refresh),
                        "access": str(access)
                    }
                    return Response(response_data)
                else:
                    return Response({'message': 'Invalid email or password'}, status=HTTP_400_BAD_REQUEST)
            else:
               return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


class UserSearchView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        offset = int(self.request.query_params.get('offset', 0))
        limit = 10
        keyword = self.request.query_params.get('search', None)
        queryset = User.objects.all()
        
        if keyword:
            queryset = queryset.filter(Q(email__iexact=keyword) | Q(username__icontains=keyword))
        
        return queryset[offset: offset + limit]
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset:
                return Response({'message': 'No users found with the given name or email'}, status=HTTP_400_BAD_REQUEST)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error in list method: {e}") 
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
        