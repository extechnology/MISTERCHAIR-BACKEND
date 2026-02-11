from MisterChairProject.urls import urlpatterns
from django.urls import path,include

urlpatterns = [
    path('auth/',include('ApplicationServices.AuthServices.auth_urls'))
]