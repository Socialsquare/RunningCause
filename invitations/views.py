
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.template import loader, Context
from django.utils.translation import ugettext as _

from .forms import EmailInviteForm
from .models import EmailInvitation


@login_required
def invite_via_email(request):

    form = EmailInviteForm()
    if request.method == 'POST':
        form = EmailInviteForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        if EmailInvitation.objects.filter(email=email,
                                          created_by=request.user).count() > 2:
            msg = _("You have already send 3 invitation to %(email)s") %\
                dict(email=email)
            messages.warning(request, msg)
            return redirect('profile:my_page')

        invitation = EmailInvitation.objects.create(
            email=email,
            created_by=request.user
        )

        invitation_sent = invitation.send(request)

        if invitation_sent:
            msg = _("You have just sent invitation to %(email)s") % {
                "email": email
            }
            messages.success(request, msg)

        return redirect('profile:my_page')
    ctx = {
        'form': form,
    }
    return render(request, 'invitations/invitation.html', ctx)
