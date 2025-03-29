from django.urls import path, include
from .views import Boil_View, Boil_View_2
from django.views.generic import TemplateView


urlpatterns = [
    path("detect", Boil_View.as_view(), name="boil_detect"),
    path("", TemplateView.as_view(template_name="boildetect/intro.html"), name="boil_intro"),
]
