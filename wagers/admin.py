from django.contrib import admin

from .models import Wager, WagerRequest

admin.site.register(Wager)
admin.site.register(WagerRequest)
