
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


from .forms import EmailInviteForm
from .models import EmailInvitation


@login_required
def invite_via_email(request):

            invite_form = EmailInviteForm(request.POST)
            if invite_form.is_valid():
                email = invite_form.cleaned_data['email']
                rate = invite_form.cleaned_data['rate']
                start_date = invite_form.cleaned_data['start_date']
                end_date = invite_form.cleaned_data['end_date']
                max_amount = invite_form.cleaned_data['max_amount']
                sponsorship = Sponsorship(runner=person,
                                          sponsor=None,
                                          rate=rate,
                                          start_date=start_date,
                                          end_date=end_date,
                                          max_amount=max_amount)
                sponsorship.save()

                email_url = reverse('sponsor_from_invite',
                                    kwargs={'sponsee_id': person.id,
                                            'sponsorship_id': sponsorship.id})

                full_email_url = request.build_absolute_uri(email_url)
                ctx = {
                    'runner': person,
                    'link': full_email_url,
                    'BASE_URL': settings.BASE_URL,
                    'title': 'Masanga Runners sponsorinvitation',
                }
                html_msg = loader.get_template('Email/email_invite.html')\
                    .render(Context(ctx))
                # FIXME: task!
                send_mail('Masanga Runners sponsorinvitation',
                          "",
                          settings.DEFAULT_FROM_EMAIL,
                          [email, ],
                          fail_silently=True,
                          html_message=html_msg)
