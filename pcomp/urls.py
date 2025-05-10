from django.urls import path
from .views import PromptInputView, FilteredPromptListView, PromptListView, HomeView, StartEC2View, PromptMetaListView

urlpatterns = [
    path('', HomeView.as_view(), name='pcomp_home'),
    path('input/', PromptInputView.as_view(), name='PromptInputView'),
    path('filtered-prompts/', FilteredPromptListView.as_view(), name='filtered_prompt_list'),
    path('prompts/', PromptListView.as_view(), name='prompt_list'),
    path('prompt-meta-list/', PromptMetaListView.as_view(), name='prompt_meta_list'),
    path('start-ec2/', StartEC2View.as_view(), name='start_ec2'),
]
