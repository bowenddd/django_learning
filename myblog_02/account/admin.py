from django.contrib import admin
from .models import UserProfile
from .models import UserInfo
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth',)
    list_filter = ('phone',)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user','school','company','profession','address','aboutme','photo')
    lsit_filter = ('school','company','profession')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserInfo,UserInfoAdmin)