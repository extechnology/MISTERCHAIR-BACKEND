from rest_framework import serializers
from .ui_models import (
    LandingImage,
    ShopByCategory,
    Category,
)   

class CategorySerializerForUI(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LandingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingImage
        fields = '__all__'

class ShopByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopByCategory
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['categories'] = CategorySerializerForUI(instance.categories, many=True).data
        return response