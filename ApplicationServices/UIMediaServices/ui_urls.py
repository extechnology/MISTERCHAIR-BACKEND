from django.urls import path
from .ui_views import (
    LandingImageAPIView,
    ShopByCategoryAPIView,
    CategoryNavItems,
)

urlpatterns = [
    path('landing-image/', LandingImageAPIView.as_view()),
    path('shop-by-category/', ShopByCategoryAPIView.as_view()),
    path('category-nav-items/', CategoryNavItems.as_view()),
]