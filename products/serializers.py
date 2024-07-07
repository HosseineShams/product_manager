from rest_framework import serializers
from .models import Product, ProductImage
from .unit_of_work import UnitOfWork

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'images']

    def validate_images(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("No more than 5 images can be uploaded.")
        for img in value:
            if img.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Each image must not exceed 2 MB.")
        return value

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        with UnitOfWork() as uow:
            product = uow.product_repository.create(validated_data)
            for image_data in images_data:
                uow.product_image_repository.create(product, image_data)
            uow.commit()
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        with UnitOfWork() as uow:
            product = uow.product_repository.update(instance, validated_data)
            uow.product_image_repository.delete_by_product(product)
            for image_data in images_data:
                uow.product_image_repository.create(product, image_data)
            uow.commit()
        return product
