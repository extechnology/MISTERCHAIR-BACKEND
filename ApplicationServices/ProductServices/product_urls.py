from django.urls import path
from .product_views import (
    ProductFilterSideBarAPIView,
    ProductFilterAPIView,
    ChairDetailAPIView,
)

urlpatterns = [
    path('filter-bar/',ProductFilterSideBarAPIView.as_view()),

    path('filter/',ProductFilterAPIView.as_view()),

    path('chair/<str:chair_id>/',ChairDetailAPIView.as_view()),
]
