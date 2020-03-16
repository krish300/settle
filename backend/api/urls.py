from django.urls import path
from django.conf.urls import url, include
from .routers import router


urlpatterns = [
    path('api/', include(router.urls))
]
