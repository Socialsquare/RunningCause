
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
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

        EmailInvitation.objects.create(
            email=email,
            created_by=request.user
        )

        ctx = {
            'BASE_URL': settings.BASE_URL,
            'link': settings.BASE_URL,
            'sender': request.user,
        }
        html_msg = loader.get_template('invitations/email/invitation.html')\
            .render(Context(ctx))
        send_mail('Masanga Runners invitation',
                  '',
                  settings.DEFAULT_FROM_EMAIL,
                  [email, ],
                  fail_silently=False,
                  html_message=html_msg)
        msg = _("You have just sent invitation to %(email)s") %\
            dict(email=email)
        messages.warning(request, msg)
        return redirect('profile:my_page')
    ctx = {
        'form': form,
    }
    return render(request, 'invitations/invitation.html', ctx)

