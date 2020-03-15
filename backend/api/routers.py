from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'entity', viewsets.EntityViewSet)
router.register(r'entity-type', viewsets.EntityTypeViewSet)
router.register(r'entry-category', viewsets.EntryCategoryViewSet)
router.register(r'entry', viewsets.EntryViewSet)
router.register(r'settlement', viewsets.SettlementViewSet)
router.register(r'cash-details', viewsets.CashDetailsViewSet)
router.register(r'sale-summary', viewsets.SaleSummaryViewSet)
router.register(r'payment-mode', viewsets.PaymentModeViewSet)