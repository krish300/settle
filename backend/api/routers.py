from rest_framework import routers
from .viewsets import EntityViewSet, EntityTypeViewSet, EntryCategoryViewSet, EntryViewSet

router = routers.DefaultRouter()
router.register(r'entity', EntityViewSet)
router.register(r'entity-type', EntityTypeViewSet)
router.register(r'entry-category', EntryCategoryViewSet)
router.register(r'entry', EntryViewSet)