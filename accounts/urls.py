from django.urls import path
from django.views.generic.base import TemplateView

from .views import SignUpView, LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup3333'),
    path("login/", LoginView.as_view(), name="login3333"),
]