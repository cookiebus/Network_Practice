from django.contrib import admin
from favorite.models import Favorite


def favoriteContent(obj):
    return obj.__unicode__()
favoriteContent.short_description = 'Content'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', favoriteContent, 'created_at')
    ordering = ('-created_at', )


admin.site.register(Favorite, FavoriteAdmin)