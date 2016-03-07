import uuid
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from common.helpers import send_email


class EmailInvitation(models.Model):
    NEW = 'new'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default=NEW)

    def send(self, request):
        context = {
            'sender': self.created_by.username,
            'link': request.build_absolute_uri(reverse('account_signup'))
        }
        emails_sent = send_email([self.email],
                                 _('Masanga Runners invitation'),
                                 'invitations/emails/invitation.html',
                                 context)
        return emails_sent == 1
