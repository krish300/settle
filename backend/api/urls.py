from django.urls import path
from django.conf.urls import url, include
from .routers import router
from . import views


urlpatterns = [
    path('api/', include(router.urls)),
    path('home/', views.home)
]
