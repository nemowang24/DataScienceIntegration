from django.urls import path, include
from .views import Boil_View

urlpatterns = [
    path("", Boil_View.as_view(), name="boil_detect"),
]


