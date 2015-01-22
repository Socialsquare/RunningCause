from django.contrib import admin
from Running.models import User, Sponsorship, Run

admin.site.register(Run)

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    readonly_fields = ('current_amount',)
    fields = ('runner', 
        'sponsor', 
        'rate',
        'email',
        'end_date',
        'max_amount',
        'active',
        'current_amount',
        )

    def current_amount(self, obj):
        amount = 0
        for payment in Payment.objects.filter(sponsorship__id=obj.id):
            amount = amount + payment.amount
        return amount