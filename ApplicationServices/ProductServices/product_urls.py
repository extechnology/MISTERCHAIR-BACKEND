from django.urls import path
from .product_views import (
    ProductFilterSideBarAPIView,
    ProductFilterAPIView,
    ChairDetailAPIView,
    RelatedProductAPIView,
    BestSellerAPIView,
)

urlpatterns = [
    path('filter-bar/',ProductFilterSideBarAPIView.as_view()),

    path('filter/',ProductFilterAPIView.as_view()),

    path('chair/<str:chair_id>/',ChairDetailAPIView.as_view()),

    path('chair/<str:chair_id>/related-products/',RelatedProductAPIView.as_view()),
    path('best-seller/',BestSellerAPIView.as_view()),
]
