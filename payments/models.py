
from django.conf import settings
from django.db import models


class PaymentLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    created_dt = models.DateTimeField(auto_now_add=True, null=False)
    amount = models.DecimalField(null=False, default=0,
                                 decimal_places=2, max_digits=10)
