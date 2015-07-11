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
def input_run(request):
    form = RunInputForm
    if request.method == "POST":
        form = RunInputForm(request.POST)
        if form.is_valid():
            distance = form.cleaned_data['distance']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date'] or start_date
            run = Run(runner=request.user, distance=distance,
                      start_date=start_date, end_date=end_date)
            run.save()
            notify_sponsors_about_run.delay(run_id=run.id)
            messages.success(request, _("Your run has been added"))
            redirect('user_runs', user_id=request.user.id)

    ctx = {
        'form': form,
    }
    return render(request, 'Running/runs/input_run.html', ctx)


@login_required
def edit_run(request, run_id):
    run = get_object_or_404(Run, pk=run_id)
    form = forms.RunInputForm(instance=run)

    print run.__dict__

    if request.user != run.runner:
        messages.error(_("You are not the owner of this run."))
        return redirect('user_view')

    if request.method == 'POST':
        form = forms.RunInputForm(request.POST, instance=run)
        if form.is_valid():
            run.distance = form.cleaned_data['distance']
            run.start_date = form.cleaned_data['start_date']
            if form.cleaned_data['end_date'] and \
                    form.cleaned_data['end_date'] >= \
                    form.cleaned_data['start_date']:
                run.end_date = form.cleaned_data['end_date']
            run.save()
            return redirect('user_runs', user_id=request.user.id)

    context = {
        'run': run,
        'form': form
    }
    return render(request, 'Running/runs/run_edit.html', context)


def user_runs(request, user_id=None):
    if not user_id:
        person = request.user
    else:
        person = get_object_or_404(User, pk=user_id)

    total_distance = person.runs.all().aggregate(x=Sum('distance'))['x'] or 0
    own_page = request.user.id == person.id

    context = {
        'person': person,
        'total_distance': total_distance,
        'runs': person.runs.all(),
        'own_page': own_page,
        'tab_name': 'runs',
    }
    return render(request, 'Running/runs/user_runs.html', context)
