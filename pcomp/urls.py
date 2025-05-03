from django.urls import path
from .views import PromptInputView, PromptListView, FilteredPromptListView

urlpatterns = [
    path('input/', PromptInputView.as_view(), name='PromptInputView'),
    path('prompts/', PromptListView.as_view(), name='prompt_list'),
    path('filtered-prompts/', FilteredPromptListView.as_view(), name='filtered_prompt_list'),
]
