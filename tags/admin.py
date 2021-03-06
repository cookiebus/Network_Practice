from django.contrib import admin
from tags.models import Tag

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'parent')
    ordering = ('-id', )


admin.site.register(Tag, TagAdmin)