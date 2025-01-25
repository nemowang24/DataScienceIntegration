from django.urls import path
from .views import intro_view

urlpatterns = [
    path("",intro_view.as_view(), name="helldivers_intro"),
]