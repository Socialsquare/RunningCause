import uuid
from django.db import models
from django.conf import settings


class EmailInvitation(models.Model):
    NEW = 'n'
    ACCEPTED = 'a'
    REJECTED = 'r'
    STATUS_CHOICES = (
        (NEW, 'new'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True,
                                      null=False)
    email = models.EmailField(unique=False, db_index=True)
    updated_dt = models.DateTimeField(auto_now=True, db_index=True)
    token = models.UUIDField(default=uuid.uuid4,
                             unique=True, db_index=True, null=False,
                             editable=False, primary_key=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                              default=NEW)
