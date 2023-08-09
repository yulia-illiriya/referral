from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from config import settings

from referral.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    
    """Модель, которая отвечает за базового юзера"""
    
    phone = models.CharField('phone number', max_length=12, unique=True)    
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=False)
    created_at = models.DateTimeField('is active', auto_now_add=True)    

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone = models.CharField('Phone number')
    name = models.CharField("Name", max_length=100, blank=True, null=True)
    surname = models.CharField("Surname", max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)
    referral_code = models.CharField("Инвайт-код", max_length=6)
    is_referral_code_activate = models.BooleanField("Использовался ли инвайт-код?", default=False)
    invite = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='invited_users', 
        null=True, 
        blank=True)         

    def __str__(self):
        return f"{self.phone}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    


