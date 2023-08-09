from django.shortcuts import redirect
from rest_framework import generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import UserProfileSerializer, UserSerializer, LoginSerializer, UserCreateSerializer
from .models import User, UserProfile


class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserVIewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer   


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():      
        phone = serializer.validated_data.get('phone')
        user_exists = User.objects.filter(phone=phone).exists()
        request.session['phone'] = phone
        
        if user_exists:                        
            return redirect("/api/v1/login/code/")
        
        serializer = UserCreateSerializer(data=serializer.validated_data) # в сериалайзере есть логика для создания пользователя
        if serializer.is_valid():
            user = serializer.save()
            return redirect("/api/v1/login/code/")        

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def enter_code(request):
    
    """Здесь вводится только код, и возвращается два токена - авторизация успешна"""
       
    phone = request.session.get('phone')
    confirm_code = request.data.get('confirm_code')
    code = '1234aa' #это код, который якобы выслан. его можно было бы хранить в сессии
    
    if code == confirm_code:
        user = User.objects.get(phone=phone)
        
        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
                    
        tokens = get_tokens_for_user(user)
        
        return Response(tokens, status=status.HTTP_200_OK) if tokens else Response({"detail": "Failed to obtain tokens"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"detail": "Invalid code", "your code": confirm_code}, status=status.HTTP_400_BAD_REQUEST)


 