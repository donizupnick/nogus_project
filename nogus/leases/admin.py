from django.contrib import admin
from .models import (
    PropertyValuation,
    PropertyImprovement,
    PropertyManagement,
    DebtFinancing,
    PropertySale,
    PropertyAcquisition,
    AreaMeasure,
    MarketLeasingProfile,
    LocationDetail,
    BuildingAreaEntry,
    LeaseFinancialDetail,
    LeaseEscalationMethod,
    rental_unit,
    RealEstateProperty,
    Lease,
    LeaseDetail,
)

admin.site.register(PropertyValuation)
admin.site.register(PropertyImprovement)
admin.site.register(PropertyManagement)
admin.site.register(DebtFinancing)
admin.site.register(PropertySale)
admin.site.register(PropertyAcquisition)
admin.site.register(AreaMeasure)
admin.site.register(MarketLeasingProfile)
admin.site.register(LocationDetail)
admin.site.register(BuildingAreaEntry)
admin.site.register(LeaseFinancialDetail)
admin.site.register(LeaseEscalationMethod)
admin.site.register(rental_unit)
admin.site.register(RealEstateProperty)
admin.site.register(Lease)
admin.site.register(LeaseDetail)
