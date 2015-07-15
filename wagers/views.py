# coding: utf8
"""
Wager is a type of a challenge.
* A runner can invite a sponsor to a wager, runner challenge itself and asks
  for sponsorship.
* A sponsor can challenge a runner by sending him a wager.

"""

import logging


from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, Context
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from .models import Wager
from .forms import WagerForm, WagerFeedbackForm, WagerChallengePreviewForm
from django.http.response import HttpResponseForbidden


log = logging.getLogger(__name__)


@login_required
def challenge_runner(request, person_id):
    """
    Sponsor creates a wager for a runner with person_id.
    """
    sponsor = request.user
    runner = get_object_or_404(get_user_model(), pk=person_id)
    if runner == sponsor:
        return HttpResponseForbidden()

    form = WagerForm()
    if request.method == "POST":
        form = WagerForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            end_date = form.cleaned_data['end_date']
            wager_text = form.cleaned_data['wager_text']

            wager = Wager.objects.create(runner=runner,
                                         sponsor=sponsor,
                                         amount=amount,
                                         end_date=end_date,
                                         wager_text=wager_text)

            link = reverse('wagers:preview_challenge',
                           kwargs={'token': wager.token.hex})
            full_link = request.build_absolute_uri(link)
            subject = _('%(username)s has challenge you') %\
                dict(username=sponsor.username)
            ctx = {
                'sponsor': sponsor.username,
                'link': full_link,
                'BASE_URL': settings.BASE_URL,
            }
            tmpl = 'wagers/emails/challenge_runner.html'
            html_msg = loader.get_template(tmpl)\
                .render(Context(ctx))
            send_mail(
                subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [runner.email],
                fail_silently=True,
                html_message=html_msg
            )
            msg = _("You have just challenge %(username)s") %\
                dict(username=runner.username)
            messages.info(request, msg)
            return redirect('profile:user_page', user_id=runner.id)

    context = {
        'runner': runner,
        'form': form,
    }
    return render(request, 'wagers/challenge_runner.html', context)


@login_required
def invite_sponsor_to_wager(request, person_id=None):
    """
    Invites a the user with person_id to sponsor a challenge for the user
    currently logged in.
    """
    runner = request.user
    sponsor = get_object_or_404(get_user_model(), pk=person_id)
    if runner == sponsor:
        return HttpResponseForbidden()

    form = WagerForm()
    if request.method == "POST":
        form = WagerForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            end_date = form.cleaned_data['end_date']
            wager_text = form.cleaned_data['wager_text']
            wager = Wager(runner=runner,
                          sponsor=sponsor,
                          amount=amount,
                          end_date=end_date,
                          wager_text=wager_text)

            wager.save()
            email_url = reverse('wagers:wager_from_invitation',
                                kwargs={'token': wager.token.hex})
            full_link = request.build_absolute_uri(email_url)
            ctx = {
                'runner': runner.username,
                'link': full_link,
            }
            tmpl = 'wagers/emails/invite_sponsor_to_wager.html'
            html_msg = loader.get_template(tmpl)\
                .render(Context(ctx))
            send_mail(_('Masanga Runners invitation for wager'),
                      '',
                      settings.DEFAULT_FROM_EMAIL,
                      [sponsor.email],
                      fail_silently=False,
                      html_message=html_msg)

            return redirect('profile:user_page', user_id=sponsor.id)
    context = {
        'person': sponsor,
        'form': form
    }
    return render(request, 'wagers/invite_sponsor_to_wager.html', context)


@login_required
def feedback_wager(request, wager_id):
    wager = get_object_or_404(Wager, pk=wager_id)
    form = WagerFeedbackForm()

    if request.method == "POST":
        if int(request.user.id) == int(wager.runner.id):

            form = WagerFeedbackForm(request.POST)

            if form.is_valid():
                update_text = form.cleaned_data['update_text']
                wager.update_text = update_text
                wager.save()
                return render(request, 'wagers/wager_update_success.html', {})

        else:
            return HttpResponseForbidden("You are not the user who recieved "
                                         "the wager! You cannot update "
                                         "this wager.")
    context = {
        'wager': wager,
        'form': form
    }
    return render(request, 'wagers/wager_update.html', context)


@login_required
def preview_challenge(request, token=None):
    """
    Runner can either accept or reject the challenge.
    """
    wager = Wager.objects.get(token=token)
    if wager.runner != request.user:
        return HttpResponseForbidden()

    form = WagerChallengePreviewForm(instance=wager)
    if request.method == 'POST':
        if request.POST.get('submit') == 'accepted':
            wager.status = wager.ACCEPTED
            email_msg = _("Runner %(username)s has accepted your challenge") %\
                dict(username=wager.runner.username)
            msg = _("You have accepted a challenge.")
        else:
            wager.status = wager.REJECTED
            email_msg = _("Runner %(username)s has rejected your challenge") %\
                dict(username=wager.runner.username)
            msg = _("You have rejected a challenge.")
        wager.save()
        messages.info(request, msg)
        send_mail(email_msg, email_msg, settings.DEFAULT_EMAIL_FROM,
                  [wager.sponsor.email, ])
        return redirect('profile:my_page')

    context = {
        'wager': wager,
        'form': form
    }
    return render(request, 'wagers/preview_challenge.html', context)


@login_required
def preview_invitation_wager(request, token=None):
    """
    Sponsor can edit wager, accept or reject invitation.
    """
    wager = Wager.objects.get(token=token)
    if wager.sponsor != request.user:
        return HttpResponseForbidden()

    form = WagerForm(instance=wager)
    if request.method == 'POST':
        if request.POST.get('submit') == 'accepted':
            wager.status = wager.ACCEPTED
            email_msg = _("Runner %(username)s has accepted your challenge") %\
                              dict(username=wager.runner.username)
            msg = _("You have accepted a challenge.")
        else:
            wager.status = wager.REJECTED
            email_msg = _("Runner %(username)s has rejected your challenge") %\
                              dict(username=wager.runner.username)
            msg = _("You have rejected a challenge.")
        wager.save()
        messages.info(request, msg)
        send_mail(email_msg, email_msg, settings.DEFAULT_EMAIL_FROM,
                  [wager.sponsor.email, ])
        return redirect('profile:my_page')

    context = {
        'wager': wager,
        'form': form
    }
    return render(request, 'wagers/preview_challenge.html', context)
