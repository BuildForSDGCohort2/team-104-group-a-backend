from rest_framework import routers
from .api import RegisterUser, LoginUser, AddMedicalData, SearchAddAndRemoveDoctor
from django.urls import path
from knox import views as KnoxView

router = routers.DefaultRouter()

urlpatterns = [
    path('login', LoginUser.as_view(), name="loginUser"),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
    path('register', RegisterUser.as_view(), name="registerUser"),
    path('addmedicaldata', AddMedicalData.as_view(), name="addMedicalData"),
    path('sarad', SearchAddAndRemoveDoctor.as_view(),
         name="searchAddAndRemoveDoctor")
]

urlpatterns += router.urls
