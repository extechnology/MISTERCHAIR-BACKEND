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
            "category": list(Category.objects.values_list("category_name", flat=True)),
            "height_stability":list(Chair.objects.values_list("height_stability", flat=True)),
            "back_support":list(Chair.objects.values_list("back_support", flat=True)),
            "capacity":list(Chair.objects.values_list("capacity", flat=True)),
            "color": [
            {
                "name": c.color_name,
                "code": list(filter(None, [c.color_code, c.color_code_2]))
            }
            for c in ChairColors.objects.all()
        ],
        }
        return Response(filter_bar, status=status.HTTP_200_OK)

class ProductFilterAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        queryset = Chair.objects.all()
        filterset = ProductFilter(request.GET, queryset=queryset)

        serializer = ChairSerializer(
            filterset.qs.distinct(),
            many=True,
            context={"request": request}
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(serializer.data, request)

        if page is None:
            return Response([], status=status.HTTP_200_OK)

        return paginator.get_paginated_response(serializer.data)

class ChairDetailAPIView(APIView):
    def get(self, request, chair_id):
        chair = Chair.objects.get(unique_id=chair_id)
        serializer = ChairSerializer(chair, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
