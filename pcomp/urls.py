from django.urls import path
from .views import PromptInputView, FilteredPromptListView, PromptListView

urlpatterns = [
    path('input/', PromptInputView.as_view(), name='PromptInputView'),
    path('filtered-prompts/', FilteredPromptListView.as_view(), name='filtered_prompt_list'),
    path('prompts/', PromptListView.as_view(), name='prompt_list'),
]
