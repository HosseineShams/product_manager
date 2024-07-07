from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Controls how many extra rows are shown for empty new entries
    max_num = 5  # Maximum number of images allowed

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'description')  
    search_fields = ('title', 'description')  
    inlines = [ProductImageInline] 

    fieldsets = (
        (None, {
            'fields': ('title', 'price', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )

admin.site.register(Product, ProductAdmin)
