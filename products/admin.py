from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  
    max_num = 5 

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'description', 'owner')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'price', 'description', 'owner')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.owner_id: 
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)  
    