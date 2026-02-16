from rest_framework import serializers
from .product_models import (
    Category,
    Chair,
    ChairColors,
    ChairImages,
    )

from .product_utils import clean_html_remove_styles


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']
    
    def to_representation(self, instance):
        return instance.category_name

class ChairImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChairImages
        fields = ['image']

    def to_representation(self, instance):
        request = self.context.get('request')
        if request:
            return f"{request.scheme}://{request.get_host()}{instance.image.url}"
        return instance.image.url


class ChairColorsSerializer(serializers.ModelSerializer):
    chair_images = ChairImagesSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    color_codes = serializers.SerializerMethodField()

    class Meta:
        model = ChairColors
        exclude = ['chair','color_code','color_code_2']
        depth = 1

    def get_discount_percentage(self, obj):
        if obj.if_discount == True and obj.is_available == True:
            discount = ((obj.price - obj.discount_price) / obj.price) * 100
            discount = round(discount, 2)
            discount = int(discount)
            if discount < 0 or discount > 100:
                return 0
            return discount
        return 0
    
    def get_color_codes(self, obj):
        return list(filter(None, [obj.color_code, obj.color_code_2]))

class ChairSerializer(serializers.ModelSerializer):
    chair_colors = ChairColorsSerializer(many=True, read_only=True)
    category = CategorySerializer()
    class Meta:
        model = Chair
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):  

        data = super().to_representation(instance)

        data['description'] = clean_html_remove_styles(data['description'])
        data['description'] = data['description'].replace("\r\n", "")
        data['description'] = data['description'].replace("\r", "")
        data['description'] = data['description'].replace("\n", "")

        data['key_features'] = clean_html_remove_styles(data['key_features'])
        data['key_features'] = data['key_features'].replace("\r\n", "")
        data['key_features'] = data['key_features'].replace("\r", "")
        data['key_features'] = data['key_features'].replace("\n", "")

        return data
