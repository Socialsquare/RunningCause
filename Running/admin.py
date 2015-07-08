from django.contrib import admin
from Running.models import User, Sponsorship, Run, Wager

admin.site.register(User)
admin.site.register(Run)
admin.site.register(Wager)

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    readonly_fields = ('current_amount', 'is_active')
    list_display = ('id', 'runner', 'sponsor', 'current_amount', 'end_date',
                    'is_active')
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
