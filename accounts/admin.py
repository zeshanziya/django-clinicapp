from django.contrib import admin
from .models import Problem

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('user', 'description')

admin.site.register(Problem, ProblemAdmin)
