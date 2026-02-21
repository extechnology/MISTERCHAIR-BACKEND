from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ApplicationServices.ProductServices.product_models import Category

from .ui_models import (
    LandingImage,
    ShopByCategory,
)
from .ui_serializers import (
    LandingImageSerializer,
    CategorySerializerForUI,
    ShopByCategorySerializer,
)


class LandingImageAPIView(APIView):
    def get(self, request):
        landing_image = LandingImage.objects.all()
        serializer = LandingImageSerializer(landing_image, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopByCategoryAPIView(APIView):
    def get(self, request):
        shop_by_category = ShopByCategory.objects.first()

        if not shop_by_category:
            return Response([], status=status.HTTP_200_OK)

        serializer = CategorySerializerForUI(
            shop_by_category.categories.all(),
            many=True,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)



class CategoryNavItems(APIView):
    def get(self, request):
        categories = Category.objects.all()

        data = []
        for category in categories:
            image_url = None
            if category.category_image:
                image_url = request.build_absolute_uri(category.category_image.url)

            data.append({
                'id': category.id,
                "category_name": category.category_name,
                "category_image": image_url
            })

        return Response(data, status=status.HTTP_200_OK)