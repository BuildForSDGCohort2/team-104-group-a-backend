from rest_framework import routers
from .api import Underconstruction
from django.urls import path

router = routers.DefaultRouter()

urlpatterns = [
  path('',Underconstruction.as_view(),name="underconstruction"),
]

urlpatterns += router.urls