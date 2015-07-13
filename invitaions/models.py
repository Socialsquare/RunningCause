import uuid
from django.db import models
from django.contrib.auth import get_user_model


class EmailInvitation(models.Model):
    NEW = 'n'
    ACCEPTED = 'a'
    REJECTED = 'r'
    STATUS_CHOICES = (
        (NEW, 'new')
        (ACCEPTED, 'accepted')
        (REJECTED, 'rejected')
    )
    created_by = models.ForeignKey(get_user_model(), null=False)
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True,
                                      null=False)
    email = models.EmailField(unique=False, db_index=True)
    updated_dt = models.DateTimeField(auto_now=True, db_index=True)
    token = models.UUIDField(default=uuid.uuid4,
                             unique=True, db_index=True, null=False,
                             editable=False, primary_key=False)
    status = models.CharField(choices=STATUS_CHOICES)
