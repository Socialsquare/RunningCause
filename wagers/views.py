# coding: utf8
"""
Wager is a type of a challenge.
* A runner can invite a sponsor to a wager, runner challenge itself and asks
  for sponsorship.
* A sponsor can challenge a runner by sending him a wager.

"""

import json
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.db import transaction

from .models import Wager, WagerRequest
from .forms import WagerForm, WagerFeedbackForm, WagerChallengePreviewForm
from django.http.response import HttpResponseForbidden, HttpResponseNotFound,\
    HttpResponseRedirect


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
            proposed_wager = json.dumps({
                'amount': form.cleaned_data['amount'],
                'end_date': form.cleaned_data['end_date'],
                'wager_text': form.cleaned_data['wager_text'],
                }, cls=DjangoJSONEncoder)

            wager_req = WagerRequest.objects.create(runner=runner,
                sponsor=sponsor, proposed_wager=proposed_wager)

            link = reverse('wagers:preview_challenge',
                           kwargs={'token': wager_req.token})
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
    Invites a user with person_id to sponsor a challenge for the user
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
            proposed_wager = json.dumps({
                'amount': form.cleaned_data['amount'],
                'end_date': form.cleaned_data['end_date'],
                'wager_text': form.cleaned_data['wager_text'],
                }, cls=DjangoJSONEncoder)

            wager_req = WagerRequest.objects.create(runner=runner,
                sponsor=sponsor, proposed_wager=proposed_wager)

            email_url = reverse('wagers:preview_invitation_wager',
                                kwargs={'token': wager_req.token.hex})
            full_link = request.build_absolute_uri(email_url)
            ctx = {
                'runner': runner.username,
                'link': full_link,
                'BASE_URL': settings.BASE_URL,
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

            messages.info(request, _("You have send invitation"
                                     " to %(username)s to challenge you.") %\
                          dict(username=wager_req.sponsor.username))
            return redirect('profile:user_page', user_id=sponsor.id)
    context = {
        'person': sponsor,
        'form': form
    }
    return render(request, 'wagers/invite_sponsor_to_wager.html', context)


class FeedbackWager(View):
    http_method_names = ['get', 'post']
    template_name = 'wagers/feedback_wager.html'
    form_class = WagerFeedbackForm

    def _check_wager_permission(self, wager):
        if self.request.user not in [wager.sponsor, wager.runner]:
            raise PermissionDenied("You cannot update this wager.")

        if self.request.user == wager.runner and wager.status != Wager.NEW:
                raise PermissionDenied("Wager has already been completed.")

        if self.request.user == wager.sponsor and\
                wager.status != Wager.COMPLETED:
            raise PermissionDenied("Wager is not completed yet.")

    def get(self, request, wager_id):
        wager = get_object_or_404(Wager, pk=wager_id)
        self._check_wager_permission(wager)
        form = self.form_class()
        ctx = {
            'wager': wager,
            'form': form,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, wager_id):
        wager = get_object_or_404(Wager, pk=wager_id)
        self._check_wager_permission(wager)

        form = self.form_class(request.POST)
        if form.is_valid():
            feedback_msg = form.cleaned_data['feedback_msg']
            if request.user == wager.runner:
                wager.runner_msg = feedback_msg
                wager.status = Wager.COMPLETED
                msg = _("Congratulations!, Your challenge will be send to"
                        " the sponsor for the final review.")
                redirect_url = reverse('profile:user_raised',
                                       kwargs=dict(user_id=request.user.id))
            elif request.user == wager.sponsor:
                wager.sponsor_msg = feedback_msg
                redirect_url = reverse('profile:user_donated',
                                       kwargs=dict(user_id=request.user.id))
                if request.POST.get('submit') == 'confirm':
                    wager.status = Wager.CONFIRMED
                    msg = _("You have accepted to pay %(username)s "
                            "for the challenge.") %\
                        dict(username=wager.runner)
                else:  # request.POST.get('submit') == 'decline':
                    wager.status = Wager.DECLINED
                    msg = _("You have declined to pay %(username)s "
                            "for the challenge.") %\
                        dict(username=wager.runner)
            wager.save()
            messages.info(request, msg)
            return HttpResponseRedirect(redirect_url)

        ctx = {
            'wager': wager,
            'form': form
        }
        return render(request, self.template_name, ctx)
feedback_wager = login_required(FeedbackWager.as_view())


@login_required
def preview_challenge(request, token=None):
    """
    Runner can either accept or reject the challenge.
    """
    wager_req = WagerRequest.objects.get(token=token)
    if wager_req.runner != request.user or\
            wager_req.status != WagerRequest.NEW:
        return HttpResponseForbidden()

    proposed = json.loads(wager_req.proposed_wager)
    form = WagerChallengePreviewForm(proposed)
    if request.method == 'POST':
        if request.POST.get('submit') == 'accept':
            wager_req.status = WagerRequest.ACCEPTED
            email_msg = _("Runner %(username)s has accepted your challenge") %\
                dict(username=wager_req.runner.username)
            msg = _("You have accepted a challenge.")
            Wager.objects.create_for_challenge(wager_req)
        else:  # request.POST.get('submit') == 'reject':
            wager_req.status = WagerRequest.REJECTED
            email_msg = _("Runner %(username)s has rejected your challenge") %\
                dict(username=wager_req.runner.username)
            msg = _("You have rejected a challenge.")
        wager_req.save()
        messages.info(request, msg)
        send_mail(email_msg, email_msg, settings.DEFAULT_FROM_EMAIL,
                  [wager_req.sponsor.email, ])
        return redirect('profile:my_page')

    context = {
        'wager_req': wager_req,
        'form': form
    }
    return render(request, 'wagers/preview_challenge.html', context)


@login_required
def preview_invitation_wager(request, token=None):
    """
    Sponsor can edit wager, accept or reject wager invitation.
    """
    wager_req = WagerRequest.objects.get(token=token)
    if wager_req.sponsor != request.user or wager_req.status != Wager.NEW:
        return HttpResponseForbidden()

    form = WagerForm(json.loads(wager_req.proposed_wager))
    if request.method == 'POST':
        form = WagerForm(request.POST)
        if form.is_valid():
            if request.POST.get('submit') == 'create':
                wager_req.status = WagerRequest.ACCEPTED
                email_msg = _("Sponsor %(username)s has challenge you!") %\
                              dict(username=wager_req.sponsor.username)
                msg = _("You have successfully created a challenge "
                        "for %(username)s.") %\
                        dict(username=wager_req.runner.username)
                Wager.objects.create_for_challenge(wager_req,
                                                   **form.cleaned_data)
            else: # request.POST.get('submit') == 'reject':
                wager_req.status = WagerRequest.REJECTED
                email_msg = _("Sponsor %(username)s has rejected your "
                              "challenge invitation.") %\
                              dict(username=wager_req.sponsor.username)
                msg = _("You have rejected a challenge invitation "
                        "from %(username)s.") %\
                    dict(username=wager_req.runner.username)
            wager_req.save()
            messages.info(request, msg)
            send_mail(email_msg, email_msg, settings.DEFAULT_FROM_EMAIL,
                      [wager_req.sponsor.email, ])
            return redirect('profile:my_page')

    context = {
        'wager_request': wager_req,
        'form': form
    }

    return render(request, 'wagers/preview_invitation_wager.html', context)
