from django.urls import include, path
from rest_framework import routers
from .tasks import API_view


# router = routers.DefaultRouter()
# router.register('counter/', API_view, basename="task")

urlpatterns = [
    path('counter/', API_view.as_view({'get': 'list', 'post':'create'}), name='counter_api'),
    # path("", include(router.urls)),
]
