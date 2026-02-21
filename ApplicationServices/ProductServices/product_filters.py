from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, CharFilter
from .product_models import Chair


class CharInFilter(BaseInFilter, CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    category = CharInFilter(
        field_name="category__category_name",
        lookup_expr="in"
    )
    height_stability = CharInFilter(lookup_expr="in")
    back_support = CharInFilter(lookup_expr="in")
    capacity = CharInFilter(lookup_expr="in")
    color = CharInFilter(
        field_name="chair_colors__color_name",
        lookup_expr="in"
    )
    is_available = filters.BooleanFilter(
        field_name="chair_colors__is_available"
    )

    min_price  = CharFilter(field_name="chair_colors__price", lookup_expr="gte")
    max_price  = CharFilter(field_name="chair_colors__price", lookup_expr="lte")
    class Meta:
        model = Chair
        fields = [
            "category",
            "height_stability",
            "back_support",
            "capacity",
            "color",
            "is_available",
            'min_price',
            'max_price'
        ]
