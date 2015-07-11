# -*- coding: utf-8 -*-
import time
import datetime
import logging

import requests
import stripe
import healthgraph
import mailchimp
from dateutil.relativedelta import relativedelta

from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, Context
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.db.models import Sum
from django.utils.translation import ugettext as _

from allauth.account.forms import LoginForm, SignupForm

from Running import forms
from Running.forms import RunInputForm
from Running.models import Sponsorship, Run, User, Wager
from Running.tasks import notify_sponsors_about_run


log = logging.getLogger(__name__)


@login_required
def make_wager(request, sponsee_id, wager_id=None):
    """
    Create a sponsorship from the person currently logged in,
    to the user with id sponsee_id.
    """
    form = forms.WagerForm
    if request.method == "POST":
        form = forms.WagerForm(request.POST)
        user_id = request.user.id
        sponsee = get_object_or_404(User, pk=sponsee_id)
        sponsor = get_object_or_404(User, pk=user_id)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            remind_date = form.cleaned_data['remind_date']
            wager_text = form.cleaned_data['wager_text']

            wager = Wager(runner=sponsee, 
                            sponsor=sponsor, 
                            amount=amount,
                            remind_date=remind_date, 
                            wager_text=wager_text)

            if wager_id != None:
                old_wager = get_object_or_404(Wager, pk = wager_id)
                old_wager.delete()
            wager.save()

            link = reverse('Running.views.user_donated', kwargs={'user_id': sponsor.id})
            full_link = request.build_absolute_uri(link)

            send_mail('Masanga Runners væddemåls-notifikation', 
                        '', 
                        settings.DEFAULT_FROM_EMAIL,
                        [sponsee.email], 
                        fail_silently=True,
                        html_message = loader.get_template('Email/wager_challenged.html').render(Context({'sponsor': sponsor.username, 
                                                                                                'link': full_link, 
                                                                                                'request': request})))

            url = reverse('Running.views.user_view', kwargs={'user_id': sponsee_id})
            return HttpResponseRedirect(url)
    invite = None

    # If this view recieved a sponsorship id, then we are filling out an invitation. If the sponsorship
    # id is valid, start out the form with the values in that sponsorship, and set invitation to be true.
    if wager_id:
        invite = get_object_or_404(Wager, pk=wager_id)
        form = forms.WagerForm(instance=invite)

    runner = get_object_or_404(User, pk=sponsee_id)

    context = {'runner': runner,
                'form': form,
                'invite': invite,
                }
    return render(request, 'Running/wager.html', context)

"""
            wager_form = forms.WagerForm(request.POST)
            if wager_form.is_valid():
                amount = wager_form.cleaned_data['amount']
                remind_date = wager_form.cleaned_data['remind_date']
                wager_text = wager_form.cleaned_data['wager_text']
                wager = Wager(runner=person,
                              sponsor=request.user,
                              amount=amount,
                              remind_date=remind_date,
                              wager_text=wager_text)
                wager.save()

                link = reverse('user_donated',
                               kwargs={'user_id': person.id})
                full_link = request.build_absolute_uri(link)
                ctx = {
                    'sponsor': person.username,
                    'link': full_link,
                }
                tname = 'Email/wager_challenged.html'
                tmpl = loader.get_template(tname)
                html_msg = tmpl.render(Context(ctx))
                # FIXME: task!
                send_mail('Masanga Runners væddemåls-notifikation',
                          '',
                          settings.DEFAULT_FROM_EMAIL,
                          [person.email, ],
                          fail_silently=True,
                          html_message=html_msg)
"""
@login_required
def invite_wager(request, sponsor_id):
    """
    Invites a the user with id sponsor_id to sponsor the user that's
    currently logged in.
    """

    sponsor = get_object_or_404(User, pk=sponsor_id)
    form = forms.InviteWagerForm
    if request.method == "POST":
        form = forms.InviteWagerForm(request.POST)
        if form.is_valid():
            sponsee = request.user
            email = sponsor.email
            amount = form.cleaned_data['amount']
            remind_date = form.cleaned_data['remind_date']
            wager_text = form.cleaned_data['wager_text']
            wager = Wager(runner=sponsee, 
                            sponsor=None, 
                            amount=amount,
                            remind_date=remind_date, 
                            wager_text=wager_text)

            wager.save()
            email_url = reverse('wager_from_invite', kwargs={'sponsee_id': sponsee.id,
                                                                'wager_id': wager.id})
            full_link = request.build_absolute_uri(email_url)
            send_mail('Masanga Runners invitation til væddemål', 
                        '',
                        settings.DEFAULT_FROM_EMAIL,
                        [email], 
                        fail_silently=True,
                        html_message = loader.get_template('Email/wager_request.html').render(Context({'runner': sponsee.username, 
                                                                                                'link': full_link,
                                                                                                'request': request})))

            url = reverse('Running.views.user_view', kwargs={'user_id': sponsor_id})
            return HttpResponseRedirect(url)
    context = {
        'sponsor': sponsor,
        'form': form
    }
    return render(request, 'Running/wager_invite.html', context)


@login_required
def update_wager(request, wager_id):
    wager = get_object_or_404(Wager, pk=wager_id)
    form = forms.WagerUpdateForm

    if request.method == "POST":
        if int(request.user.id) == int(wager.runner.id):

            form = forms.WagerUpdateForm(request.POST)

            if form.is_valid():
                update_text = form.cleaned_data['update_text']
                wager.update_text = update_text
                wager.save()
                return render(request, 'Running/wager_update_success.html', {})

        else:
            return HttpResponse("You are not the user who recieved the wager! You cannot update this wager.")
    context = {
        'wager': wager,
        'form': form
    }

    return render(request, 'Running/wager_update.html', context)


@login_required
def confirm_wager(request, wager_id):
    wager = get_object_or_404(Wager, pk=wager_id)
    if int(request.user.id) == int(wager.sponsor.id):
        wager.fulfilled = True
        wager.save()
        return render(request, 'Running/wager_confirm_success.html', {})
    return HttpResponse("You are not the user who gave the wager! You cannot confirm this wager.")


@login_required
def decline_wager(request, wager_id):
    wager = get_object_or_404(Wager, pk=wager_id)
    if int(request.user.id) == int(wager.sponsor.id):
        wager.delete()
        return render(request, 'Running/wager_deny_success.html', {})
    return HttpResponse("You are not the user who gave the wager! You cannot decline this wager.")
