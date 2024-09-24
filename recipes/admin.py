from django.contrib import admin
from .models import Category , Recipe

class CategoryaAdmin(admin.ModelAdmin):
    ...

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Category ,CategoryaAdmin)