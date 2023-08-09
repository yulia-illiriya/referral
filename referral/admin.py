from django.contrib import admin

from referral.models import UserProfile, User

admin.site.register(User)
admin.site.register(UserProfile)
