from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
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
        user_model = get_user_model()
        try:
            existing_user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            existing_user = None

        if existing_user:
            msg = _('The person you are inviting already has a profile')
            messages.warning(request, msg)
            return redirect('profile:overview', user_id=existing_user.id)

        invitations = EmailInvitation.objects.filter(email=email,
                                                     created_by=request.user)
        if invitations.count() > 2:
            msg = _("You have already send 3 invitation to %(email)s") % {
                'email': email
            }
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
