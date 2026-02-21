from django.urls import path,include

urlpatterns = [
    path('auth/',include('ApplicationServices.AuthServices.auth_urls')),
    path('chairs/',include('ApplicationServices.ProductServices.product_urls')),
    path('ui/',include('ApplicationServices.UIMediaServices.ui_urls'))
]