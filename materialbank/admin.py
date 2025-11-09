from django.contrib import admin

# Register your models here.
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'donator_name', 'current_with', 'added_on')
    search_fields = ('name', 'donator_name', 'current_with')
    list_filter = ('category',)

from .models import Points

@admin.register(Points)
class PointsAdmin(admin.ModelAdmin):
    list_display = ('email', 'total_points')
