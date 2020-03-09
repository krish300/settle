from rest_framework import routers
from .viewsets_api import EntityViewSet, EntityTypeViewSet, EntryCategoryViewSet
from .viewsets_auth import AuthViewSet


router = routers.DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')
router.register(r'entity', EntityViewSet)
router.register(r'entity-type', EntityTypeViewSet)
router.register(r'entry-category', EntryCategoryViewSet)
