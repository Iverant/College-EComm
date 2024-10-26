from django.contrib import admin
from .models import Product
# Register your models here.

admin.site.site_header = 'E-commerce Admin'
admin.site.site_title = 'E-commerce Admin Portal'
admin.site.index_title = 'Welcome to E-commerce Admin Portal'

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'desc','quantity']
    search_fields = ['name', ]


    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)
    
    actions = ['set_price_to_zero',]
    list_editable = ['desc', 'price','quantity']

admin.site.register(Product, ProductAdmin)