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
from .models import Run
from .tasks import notify_sponsors_about_run


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
            redirect('runs:user_runs', user_id=request.user.id)

    ctx = {
        'form': form,
    }
    return render(request, 'runs/input_run.html', ctx)


@login_required
def edit_run(request, run_id):
    run = get_object_or_404(Run, pk=run_id)
    form = RunInputForm(instance=run)

    print run.__dict__

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

    # This means the user hasn't previously registered with runkeeper, but is just coming back from getting
    # a runkeeper access token code. Get that code from the GET data, and use that to get get an
    # access token, which you can then use to access all of their workouts.
    # Then, create a run object for each workout that does not currently have
    # a run object.
    if request.GET.has_key('code'):

        # Get the code from the GET data. This will allow us to get an access
        # token.
        code = request.GET['code']

        # Create an instance of the healthgraph API.
        rk_auth_mgr = healthgraph.AuthManager(settings.RUNKEEPER_CLIENT_ID,
                                              settings.RUNKEEPER_CLIENT_SECRET,
                                              settings.APP_URL + reverse('Running.views.register_runkeeper',
                                                                         kwargs={'runner_id': request.user.id})
                                              )

        # Get the access token using the code and the instance of the
        # healthgraph API.
        access_token = rk_auth_mgr.get_access_token(code)

        # Associate the token with the user, and save.
        request.user.access_token = access_token
        request.user.save()

        # Now that we've associated the token with the user, we're done with authentication.
        # Call this view again to finally deal with the workout data.
        url = reverse('register_runkeeper',
                      kwargs={'runner_id': request.user.id})
        return HttpResponseRedirect(url)

    # This means that the user has registered with runkeeper before, and has an access token.
    # Use this to get the workouts for the user, and create and store new run objects for
    # every run that has not been previously registered with runkeeper.
    elif request.user.access_token:

        # Request the workout data for the user using our new, shiny access
        # token.
        r = requests.get('https://api.runkeeper.com/fitnessActivities',
                         headers={'Authorization': 'Bearer %s' %
                                  request.user.access_token}
                         )

        # Convert the workout data from JSON to make it easier to work with.
        data = r.json()

        # Get all runs that are associated with the user, and that came from runkeeper.
        # Compile all the of the source ids for them (the ids that were given to them
        # by their source, in this case runkeeper). This is important so that we make
        # sure that we don't register the same run multiple times.
        runkeeper_runs = request.user.runs.filter(source="runkeeper")
        registered_ids = [run.source_id for run in runkeeper_runs]

        # For each workout in the returned data...
        for item in data['items']:

            # If the workout hasn't already been registered with us...
            if item['uri'] not in registered_ids:

                # This coming block of code looks terrible. Unfortunately, there's not much
                # we can do about that.

                # Check to see how long the start_time item is. Here's why: the runkeeper API
                # does make some effort to make sure that their dates are easily machine readable
                # (the months are 3 letter abreviations, etc.). Unfortunately, they don't pad the
                # day of the month to make sure it's 2 digits. So, they'll return 11, 21, 31, but
                # will also return 1 instead of 01. This is the only thing that changes length in
                # in the whole date format, so you're gonna wann look out for that. If the day of
                # the month has 1 digit, then the whole string has length 24. Otherwise, it has
                # length 25.
                if len(item['start_time']) == 24:

                    # Here, we're making a datetime object from our string using the strptime function.
                    # You may notice the "[5:15]" section of this line. This is because the date contains
                    # a lot of information that's not useful to us, so we're just stripping this out.
                    # We're making a datetime assuming the format day of the month, month abbreviation, and
                    # 4 digit year.
                    date = time.strptime(item['start_time'][5:15], "%d %b %Y")

                # This means we've gotten a 2 digit day of the month. Proceed as above, just stripping
                # differently.
                else:

                    # Here, we're making a datetime object from our string using the strptime function.
                    # You may notice the "[5:16]" section of this line. This is because the date contains
                    # a lot of information that's not useful to us, so we're just stripping this out.
                    # We're making a datetime assuming the format day of the month, month abbreviation, and
                    # 4 digit year.
                    date = time.strptime(item['start_time'][5:16], "%d %b %Y")

                # This line is terrible. However, it works, and it works well. This creates a new date object
                # from the datetime object we just created.
                date = datetime.datetime(*date[:6]).date()

                # Create a new run object from the information we've assembled about the workout, and save it.
                # The distance value is divided by 1000 because runkeeper gives the distance in metres,
                # while our website stores them as kilometers.
                new_run = Run(runner=request.user,
                              distance=item['total_distance'] / 1000,
                              start_date=date,
                              end_date=date,
                              source="runkeeper",
                              source_id=item['uri'])
                new_run.save()

        return redirect('profile:my_page')

    # If the user has no code, and no token associated with their account, we need to start the
    # authentication process from scratch.
    else:

        # Create an instance of the healthgraph API.
        rk_auth_mgr = healthgraph.AuthManager(settings.RUNKEEPER_CLIENT_ID,
                                              settings.RUNKEEPER_CLIENT_SECRET,
                                              settings.APP_URL + reverse('register_runkeeper',
                                                                         kwargs={'runner_id': request.user.id}))

        # Get the uri that should be accessed to get the code, and redirect
        # there.
        rk_auth_uri = rk_auth_mgr.get_login_url()
        return HttpResponseRedirect(rk_auth_uri)
