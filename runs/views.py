# coding: utf8
import time
import datetime
import logging

import requests
import healthgraph

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.db.models import Sum
from django.utils.translation import ugettext as _

from .forms import RunInputForm
from .models import Run, RunkeeperToken
from .tasks import notify_sponsors_about_run, pull_user_runs_from_runkeeper


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
            return redirect('runs:user_runs', user_id=request.user.id)

    ctx = {
        'form': form,
    }
    return render(request, 'runs/input_run.html', ctx)


@login_required
def edit_run(request, run_id):
    run = get_object_or_404(Run, pk=run_id)
    form = RunInputForm(instance=run)

    if request.user != run.runner:
        messages.error(_("You are not the owner of this run."))
        return redirect('home')

    if request.method == 'POST':
        form = RunInputForm(request.POST, instance=run)
        if form.is_valid():
            run.distance = form.cleaned_data['distance']
            run.start_date = form.cleaned_data['start_date']
            if form.cleaned_data['end_date'] and \
                    form.cleaned_data['end_date'] >= \
                    form.cleaned_data['start_date']:
                run.end_date = form.cleaned_data['end_date']
            run.save()
            return redirect('runs:user_runs', user_id=request.user.id)

    context = {
        'run': run,
        'form': form
    }
    return render(request, 'runs/run_edit.html', context)


def user_runs(request, user_id=None):
    if not user_id:
        if not request.user.is_authenticated():
            return redirect('profile:signup_or_login')
        person = request.user
    else:
        person = get_object_or_404(get_user_model(), pk=user_id)

    total_distance = person.runs.all().aggregate(x=Sum('distance'))['x'] or 0
    own_page = request.user.id == person.id

    context = {
        'person': person,
        'total_distance': total_distance,
        'runs': person.runs.all(),
        'own_page': own_page,
        'tab_name': 'runs',
    }
    return render(request, 'runs/user_runs.html', context)


@login_required
def register_runkeeper(request):
    """
    Overall, update the runs of the users to reflect their runkeeper account.
    This can take a few forms.
    -   If they haven't previously registered with runkeeper, request an
        access code through the healthgraph
        api. Have runkeeper redirect to this url, so that we can have
        the possibility below.
    -   If they haven't previously registered with runkeeper, but the request
        has a value 'code' in the GET
        data, the first possibilty has been called, and has returned to this.
        User this code to get an
        access token for the user, save it with the user, and call this method
        again to actually deal
        with the workout data.
    -   If the user accesses this url with a runkeeper token, our job is much
        easier. Just access this token,
        use it to get all the workout data for the user, and use create new
        run objects for each workout 
        that does not currently have a run object.
    """

    # This means the user hasn't previously registered with runkeeper,
    # but is just coming back from getting
    # a runkeeper access token code. Get that code from the GET data, and use that to get get an
    # access token, which you can then use to access all of their workouts.
    # Then, create a run object for each workout that does not currently have
    # a run object.
    if request.GET.has_key('code'):

        # Get the code from the GET data. This will allow us to get an access
        # token.
        code = request.GET['code']

        # Create an instance of the healthgraph API.
        rk_auth_mgr = healthgraph.AuthManager(
            settings.RUNKEEPER_CLIENT_ID,
            settings.RUNKEEPER_CLIENT_SECRET,
            settings.BASE_URL +
            reverse('runs.register_runkeeper')
        )

        # Get the access token using the code and the instance of the
        # healthgraph API.
        access_token = rk_auth_mgr.get_access_token(code)

        # Associate the token with the user, and save.
        request.user.access_token = access_token
        request.user.save()
        RunkeeperToken.objects.create(runner=request.user,
                                      access_token=access_token)

        # Now that we've associated the token with the user, we're done with authentication.
        # Call this view again to finally deal with the workout data.
        return redirect('runs:register_runkeeper')

    # This means that the user has registered with runkeeper before, and has an access token.
    # Use this to get the workouts for the user, and create and store new run objects for
    # every run that has not been previously registered with runkeeper.
    elif RunkeeperToken.objects.filter(runner_id=request.user.id).count():
        pull_user_runs_from_runkeeper.delay(user_id=request.user.id)
        messages.info(request, _("Your runs from RunKeeper are"
                                 " being process..."))
        return redirect('profile:my_page')

    # If the user has no code, and no token associated with their account, we need to start the
    # authentication process from scratch.
    else:

        # Create an instance of the healthgraph API.
        rk_auth_mgr = healthgraph.AuthManager(
            settings.RUNKEEPER_CLIENT_ID,
            settings.RUNKEEPER_CLIENT_SECRET,
            settings.BASE_URL + reverse('runs:register_runkeeper'))

        # Get the uri that should be accessed to get the code, and redirect
        # there.
        rk_auth_uri = rk_auth_mgr.get_login_url()
        return HttpResponseRedirect(rk_auth_uri)
