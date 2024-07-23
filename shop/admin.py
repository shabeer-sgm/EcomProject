from django.contrib import admin
from . models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display =('name' , 'image' , 'description')

class ProductAdmin(admin.ModelAdmin):
    list_display =('name' , 'products_image' , 'quantity', 'original_price' , 'selling_price' , 'trending')     
    
admin.site.register(Category , CategoryAdmin)
admin.site.register(Product , ProductAdmin )
