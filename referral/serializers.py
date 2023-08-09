import random
import time
from rest_framework import serializers
from django.db import transaction
from .utils import generate_random_invite_code
from referral.models import UserProfile, User


class LoginSerializer(serializers.Serializer):
    
    """Сериалайзер для начала входа"""
    
    phone = serializers.CharField()


class UserCreateSerializer(serializers.ModelSerializer):
    
    """просто создаем юзера на основе телефона"""
    
    class Meta:
        model = User        
        fields = ['phone']


    def create(self, validated_data):        
               
        user = User.objects.create_user(
            phone=validated_data['phone'],                      
        )
        
        UserProfile.objects.create(
            user=user,
            phone=validated_data['phone'],
            referral_code=generate_random_invite_code()
        )
        
        return user
    

class UserSerializer(serializers.ModelSerializer):
    
    """Вместо пароля вводится код, который надо сравнить с тем, что у нас хранится"""
    
    code = serializers.CharField(write_only=True)
    confirm_code = serializers.CharField(write_only=True)
    
    class Meta:
        model = User        
        fields = ['phone', 'code', 'confirm_code']


class SimpleUserProfileSerializer(serializers.ModelSerializer):
    
    """
    Простой сериалайзер, который выводит 
    только нужные нам поля без вложенностей
    """
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    
    """
    Основной сериалайзер, который сериализует все поля и 
    добавляет информацию о юзере и о том, чей код он использовал
    и кто использовал его
    """
    
    invited_users = serializers.SerializerMethodField()
    invited_by = serializers.SerializerMethodField()
    referral_code = serializers.ReadOnlyField()
    is_referral_code_activate = serializers.ReadOnlyField()    

    class Meta:
        model = UserProfile
        fields = [
            'referral_code', 
            'invited_users', 
            'invited_by', 
            'user', 
            'phone', 
            'name', 
            'surname', 
            'photo', 
            'is_referral_code_activate'
            ]        
        
        
    def get_invited_users(self, user_profile):
        
        """Получаем приглашенных нами юзеров"""
        
        invited_users = UserProfile.objects.filter(invite=user_profile)
        return SimpleUserProfileSerializer(invited_users, many=True).data

    def get_invited_by(self, user_profile):
        
        """
        Получаем пригласившего нас юзера
        """
                
        return SimpleUserProfileSerializer(user_profile.invite).data if user_profile.invite else None
    
    def validate(self, data):
        invited_code = self.context['request'].data.get('invited_by')
        
        try:
            invited_by_user = UserProfile.objects.get(referral_code=invited_code)
            data['invited_by'] = invited_by_user
        except UserProfile.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code")

        data['invited_by'] = invited_by_user

        return data
    
    def update(self, instance, validated_data):
        
        """
        Переопределяем функцию обновления.
        Профиль создается автоматически, поэтому 
        метода добавления нет
        """
        
        invited_by = validated_data['invited_by']
        
        print(validated_data)
        print(invited_by)
        
        if invited_by:
            instance.invite = invited_by  # Создаем связь через внешний ключ
            instance.is_referral_code_activate = True

        instance.phone = validated_data.get('phone', instance.phone)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.photo = validated_data.get('photo', instance.photo)
        
        instance.save()

        return instance
          
          
    
