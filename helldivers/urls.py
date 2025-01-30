from django.urls import path, include
from .views import Intro_view, Practice_view, Statistic_view


from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'counter/', TaskViewSet2, basename="task")

urlpatterns = [

    path("practice/", Practice_view.as_view(), name="helldivers_practice"),
    # path('api/counter/', views.api_counter, name='counter_api'),
    path("intro/", Intro_view.as_view(), name="helldivers_intro"),

    path("statistic/", Statistic_view.as_view(), name="counter_statistic"),
    # path("", include(router.urls)),
]



# if settings.DEBUG:  # Allows debug_toolbar only in DEBUG mode
#     import debug_toolbar
#
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
