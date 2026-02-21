from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ApplicationServices.paginations import StandardResultsSetPagination
from .product_serializers import (
    CategorySerializer,
    ChairSerializer,
    ChairColorsSerializer,
    ChairImagesSerializer,
    )

from .product_models import (
    Category,
    Chair,
    ChairColors,
    ChairImages,
    )

from .product_filters import ProductFilter


class ProductFilterSideBarAPIView(APIView):
    def get(self, request):
        filter_bar = {
            "category": list(Category.objects.values_list("category_name", flat=True).distinct()),
            "height_stability":list(Chair.objects.values_list("height_stability", flat=True).distinct()),
            "back_support":list(Chair.objects.values_list("back_support", flat=True).distinct()),
            "capacity":list(Chair.objects.values_list("capacity", flat=True).distinct()),
            "color": [
                {
                    "name": c["color_name"],
                    "code": list(
                        filter(None, [c["color_code"], c["color_code_2"]])
                    )
                }
                for c in ChairColors.objects.values(
                    "color_name", "color_code", "color_code_2"
                ).distinct()
            ],
        }
        return Response(filter_bar, status=status.HTTP_200_OK)

class ProductFilterAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        queryset = Chair.objects.all()
        filterset = ProductFilter(request.GET, queryset=queryset)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(
            filterset.qs.distinct(),
            request
        )

        if page is None:
            serializer = ChairSerializer(
                filterset.qs.distinct(),
                many=True,
                context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = ChairSerializer(
            page,
            many=True,
            context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)

class ChairDetailAPIView(APIView):
    def get(self, request, chair_id):
        chair = Chair.objects.get(unique_id=chair_id)
        serializer = ChairSerializer(chair, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RelatedProductAPIView(APIView):
    def get(self, request, chair_id):
        chair = Chair.objects.get(unique_id=chair_id)
        related_products = Chair.objects.filter(category=chair.category).exclude(unique_id=chair_id)
        serializer = ChairSerializer(related_products, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BestSellerAPIView(APIView):
    def get(self, request):
        best_seller = Chair.objects.filter(special_tag='Bestseller').order_by('-created_at')[:6]
        serializer = ChairSerializer(best_seller, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)