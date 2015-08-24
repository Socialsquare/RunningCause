# coding: utf8
import json
from datetime import date

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.template import loader, Context
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _
from django.core.serializers.json import DjangoJSONEncoder

from .models import Sponsorship, SponsorRequest
from .forms import SponsorForm


@login_required
def end_sponsorship(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorship, pk=sponsorship_id)

    if request.user == sponsorship.sponsor or \
            request.user == sponsorship.runner:
        sponsorship.end_date = date.today()
        sponsorship.save()
        messages.success(request, _("Sponsorship has been ended."))
        return redirect('profile:user_donated', user_id=request.user.id)

    messages.error(request,
                   _("You are not a associated with this sponsorship."))
    return redirect('profile:my_page')


@login_required
def add_sponsorship(request, runner_id=None):
    """
    Create a sponsorship from a person currently logged in (sponsor),
    to a runner with given runner_id (user id).
    """
    runner = get_object_or_404(get_user_model(), pk=runner_id)
    sponsor = request.user
    form = SponsorForm()
    if request.method == "POST":
        form = SponsorForm(request.POST)
        if form.is_valid():
            rate = form.cleaned_data['rate']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            max_amount = form.cleaned_data['max_amount']
            sponsorship = Sponsorship(runner=runner,
                                      sponsor=sponsor,
                                      rate=rate,
                                      start_date=start_date,
                                      end_date=end_date,
                                      max_amount=max_amount)
            sponsorship.save()
            messages.success(request,
                             _("Your sponsorship of %(username)s has "
                                        "been set up.") % \
                             dict(username=runner.username))
            return redirect('profile:user_donated', user_id=sponsor.id)

    context = {
        'runner': runner,
        'form': form,
    }
    return render(request, 'sponsorship/add_sponsorship.html', context)


@login_required
def request_sponsorship(request, person_id):
    sponsor = get_object_or_404(get_user_model(), id=person_id)
    runner = request.user
    form = SponsorForm()
    if request.method == "POST":
        form = SponsorForm(request.POST)
        if form.is_valid():
            proposed = json.dumps({
                'rate': form.cleaned_data['rate'],
                'start_date': form.cleaned_data['start_date'],
                'end_date': form.cleaned_data['end_date'],
                'max_amount': form.cleaned_data['max_amount'],
            }, cls=DjangoJSONEncoder)

            sponsor_req = SponsorRequest.objects\
                .create(runner=runner,
                        sponsor=sponsor,
                        proposed_sponsorship=proposed)
            email_url = reverse('sponsorship:add_sponsorship_from_request',
                                kwargs={'token': sponsor_req.token})
            full_email_url = request.build_absolute_uri(email_url)
            title = _('Masanga Runners sponsorship request')
            ctx = {
                'runner': runner,
                'link': full_email_url,
                'BASE_URL': settings.BASE_URL,
                'title': title,
            }
            tmpl = 'sponsorship/email/request_sponsorship.html'
            html_msg = loader.get_template(tmpl).render(Context(ctx))
            send_mail(title,
                      "",
                      settings.DEFAULT_FROM_EMAIL,
                      [sponsor.email, ],
                      fail_silently=True,
                      html_message=html_msg)
            messages.info(request, _("We have sent your request to sponsor."))
            return redirect('profile:user_donated', user_id=person_id)

    ctx = {
        'form': form,
        'runner': runner,
        'sponsor': sponsor,
    }
    return render(request, 'sponsorship/request_sponsorship.html', ctx)


@login_required
def add_sponsorship_from_request(request, token=None):
    sponsor = request.user
    sp_req = get_object_or_404(SponsorRequest, token=token)
    runner = sp_req.runner
    if sponsor != sp_req.sponsor:
        return HttpResponseForbidden()

    form = SponsorForm(json.loads(sp_req.proposed_sponsorship))
    if request.method == "POST":
        form = SponsorForm(request.POST)
        if form.is_valid():
            rate = form.cleaned_data['rate']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            max_amount = form.cleaned_data['max_amount']
            sponsorship = Sponsorship.objects.create(runner=runner,
                                                     sponsor=sponsor,
                                                     rate=rate,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     max_amount=max_amount)
            SponsorRequest.objects.filter(token=token)\
                .update(sponsorship=sponsorship)
            return redirect('profile:user_donated', user_id=sponsor.id)
    ctx = {
        'form': form,
        'sponsor': sponsor,
        'runner': runner,
    }
    return render(request, 'sponsorship/add_sponsorship.html', ctx)
