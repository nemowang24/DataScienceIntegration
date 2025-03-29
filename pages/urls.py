from django.urls import path

from .views import HomePageView, PresignedUrlView, ChurnAnalysisView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),

    path("churnanalysis/", ChurnAnalysisView.as_view(), name="churnanalysis1"),

    path('get-pdf-url/<str:file_name>/', PresignedUrlView.as_view(), name='generate_presigned_url'),
]
