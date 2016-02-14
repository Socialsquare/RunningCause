from django.contrib import admin

from .models import Sponsorship, SponsorRequest


@admin.register(SponsorRequest)
class SponsorRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    readonly_fields = ('total_amount', 'is_active')
    list_display = ('id', 'runner', 'sponsor', 'total_amount', 'end_date',
                    'max_amount', 'amount_paid', 'is_active')
    fields = (
        'sponsor',
        'runner',
        'rate',
        'end_date',
        'max_amount',
        'amount_paid',
        'total_amount',
        'is_active',
    )

    def total_amount(self, obj):
        return obj.total_amount

    def is_active(self, obj):
        return obj.is_active
