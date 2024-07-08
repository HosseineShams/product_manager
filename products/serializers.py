from rest_framework import serializers
from .models import Product, ProductImage
from .unit_of_work import UnitOfWork

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:  
            raise serializers.ValidationError("Each image must not exceed 2 MB.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'images']

    def validate_images(self, data):
        if len(data) > 5:  
            raise serializers.ValidationError("No more than 5 images can be uploaded.")
        return data

    def to_internal_value(self, data):
        images_data_files = data.getlist('images') if 'images' in data else []
        
        if len(images_data_files) > 5:
            raise serializers.ValidationError({"images": "No more than 5 images can be uploaded."})
        
        for image_file in images_data_files:
            serializer = ProductImageSerializer(data={'image': image_file})
            if not serializer.is_valid():
                raise serializers.ValidationError({"images": serializer.errors['image']})

        validated_data = super().to_internal_value({key: value for key, value in data.items() if key != 'images'})
        validated_data['images'] = images_data_files
        return validated_data

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        with UnitOfWork() as uow:
            validated_data['owner'] = self.context['request'].user 
            product = uow.product_repository.create(validated_data)
            for image_data in images_data:
                uow.product_image_repository.create(product, {'image': image_file})
            uow.commit()
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        with UnitOfWork() as uow:
            product = uow.product_repository.update(instance, validated_data)
            uow.product_image_repository.delete_by_product(instance) 
            for image_data in images_data:
                uow.product_image_repository.create(instance, {'image': image_data})
            uow.commit()
        return instance
