from django.contrib import admin
from .models import Product 

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available', 'created_at', 'updated_at')
    list_editable = ('price', 'stock', 'is_available')
    list_per_page = 20
    search_fields = ('product_name', 'category__category_name')
    list_filter = ('is_available', 'category')
admin.site.register(Product, ProductAdmin)
