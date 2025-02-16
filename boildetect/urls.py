from django.urls import path, include
from .views import Boil_View, Boil_View_2

urlpatterns = [
    path("", Boil_View.as_view(), name="boil_detect"),
    path("b/", Boil_View_2.as_view(), name="boil_detect2"),
]
