from rest_framework import routers
from .viewsets import EntityViewSet, EntityTypeViewSet, EntryCategoryViewSet

router = routers.DefaultRouter()
router.register(r'entity', EntityViewSet)
router.register(r'entity-type', EntityTypeViewSet)
router.register(r'entry-category', EntryCategoryViewSet)