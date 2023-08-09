from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserProfileView, UserVIewSet, login, enter_code


router = DefaultRouter()
router.register(r'user-profiles', UserProfileView)
router.register(r'users', UserVIewSet)

urlpatterns = [    
    path('profile/', include(router.urls), name="profile"),
    path('login/', login, name='login'),
    path('login/code/', enter_code, name="tokens"),    
]