from django.urls import path
from .views import PromptInputView

urlpatterns = [
    path('input/', PromptInputView.as_view(), name='PromptInputView'),
]