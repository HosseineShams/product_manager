from .models import Product, ProductImage
# 
class ProductRepository:
    def create(self, product_data):
        return Product.objects.create(**product_data)

    def get_by_id(self, product_id):
        return Product.objects.get(id=product_id)

    def update(self, product, updated_data):
        for key, value in updated_data.items():
            setattr(product, key, value)
        product.save()
        return product

    def delete(self, product):
        product.delete()

class ProductImageRepository:
    def create(self, product, image_data):
        return ProductImage.objects.create(product=product, **image_data)

    def delete_by_product(self, product):
        ProductImage.objects.filter(product=product).delete()
