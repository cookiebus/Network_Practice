from django.contrib import admin
from users.models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'birthday', 'description', 'profile_image')
    list_filter = ('id', 'user')
    ordering = ('-id', )

    filter_horizontal = ('friends', )


admin.site.register(UserProfile, UserProfileAdmin)