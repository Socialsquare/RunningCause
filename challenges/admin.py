from django.contrib import admin

from .models import Challenge, ChallengeRequest

admin.site.register(Challenge)
admin.site.register(ChallengeRequest)
