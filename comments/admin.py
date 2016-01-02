from django.contrib import admin
from comments.models import Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reply_user', 'problem', 'description')
    ordering = ('-id', )


admin.site.register(Comment, CommentAdmin)