from django.contrib import admin
from Running.models import User, Sponsorship, Run

admin.site.register(User)
admin.site.register(Run)

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    readonly_fields = ('current_amount', 'is_active')
    fields = ('runner', 
        'sponsor', 
        'rate',
        'end_date',
        'max_amount',
        'current_amount',
        'is_active',
        )

    def current_amount(self, obj):
        return obj.total_amount

    def is_active(self, obj):
        return obj.is_active