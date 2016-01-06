from django.contrib import admin
from problems.models import Problem

# Register your models here.
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'problem_image', 'description', 'up', 'x', 'y')
    ordering = ('-id', )
    filter_horizontal = ('tags', )


admin.site.register(Problem, ProblemAdmin)