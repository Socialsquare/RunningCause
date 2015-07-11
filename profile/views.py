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
stripe.api_key = settings.STRIPE_SECRET_KEY



@login_required
def sign_in_landing(request):
    user = request.user
    if user.newsletter:
        try:
            m = mailchimp.Mailchimp(settings.COURRIERS_MAILCHIMP_API_KEY)
            m.lists.subscribe('2640511eac', {'email': user.email})
            user.newsletter = False
            user.save()
            messages.success(
                request,  _("The email has been successfully subscribed"))
        except mailchimp.ListAlreadySubscribedError:
            messages.error(
                request,  _("That email is already subscribed to the list"))
            return HttpResponseRedirect('/')
        except mailchimp.Error as e:
            log.error("mailchimp error: %s, %s", e.__class__, e)
            messages.error(request,  _("An error occurred while subscribing"
                                       " to mailing list."))
            return HttpResponseRedirect('/')

    if not user.greeted:
        user.greeted = True
        user.save()
        url = reverse('account:credit_card_prompt')
        return HttpResponseRedirect(url)
    url = reverse('Running.views.home')
    return HttpResponseRedirect(url)


@login_required
def credit_card_prompt(request):
    ctx = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'email': request.user.email
    }
    return render(request, 'Running/credit_card_prompt.html', ctx)


@login_required
@csrf_exempt
def register_customer(request):
    token = request.POST['stripeToken']
    customer = stripe.Customer.create(source=token,
                                      description=request.user.username)
    request.user.stripe_customer_id = customer.id
    request.user.save()
    return render(request, 'Running/credit_card_success.html', {})


@login_required
def unsubscribe(request):
    user = request.user
    user.subscribed = False
    user.save()
    return render(request, 'Running/unsubscribed_success.html', {})


@login_required
def subscribe(request):
    user = request.user
    user.subscribed = True
    user.save()
    return render(request, 'Running/subscribed_success.html', {})


@login_required
def unregister_card(request):
    user = request.user
    user.stripe_customer_id = None
    user.save()
    return render(request, 'Running/deregister_success.html', {})


@cache_page(60 * 1)  # cache it for 1 minute
def info_widget(request):
    all_users = User.objects.all()

    num_runners = len([us.id for us in all_users if us.is_runner])
    num_sponsors = len([us.id for us in all_users if us.is_sponsor])

    spships = Sponsorship.objects.all().exclude(sponsor__isnull=True)
    amount_donated = sum([sp.amount_paid for sp in spships])

    wagers = Wager.objects.filter(paid=True)
    amount_donated += sum([wager.amount for wager in wagers])

    total_distance = Run.objects.all().aggregate(x=Sum('distance'))['x'] or 0

    context = {
        'num_runners': num_runners,
        'num_sponsors': num_sponsors,
        'amount_donated': amount_donated,
        'total_distance': total_distance,
    }
    return render(request, 'Running/info_widget.html', context)


def user_view(request, user_id):
    """
    Redirects to a page for a specific user, displaying their username and all
    their sponsorships.
    """
    user = get_object_or_404(User, pk=user_id)
    if (request.user.is_authenticated() and
            int(user.id) == int(request.user.id)) or \
            user.is_public:
        url = reverse('user_runs', kwargs={'user_id': user_id})
    else:
        url = reverse('user_raised', kwargs={'user_id': user_id})
    return HttpResponseRedirect(url)


@login_required
def user_settings(request):
    return render(request, 'Running/user_settings.html', {})


@login_required
def my_page(request):
    url = reverse('Running.views.user_view', kwargs={'user_id': request.user.id})
    return HttpResponseRedirect(url)


@login_required
def make_profile_public(request):
    request.user.is_public = True
    request.user.save()
    messages.info(request, _("Your settings has been saved."))
    return redirect('user_settings')


@login_required
def make_profile_private(request):
    request.user.is_public = False
    request.user.save()
    messages.info(request, _("Your settings has been saved."))
    return redirect('user_settings')


def signup_or_login(request):
    context = {
        'form': LoginForm,
        'signup_form': SignupForm
    }
    return render(request, 'Running/signup_or_login.html', context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def overview(request):
    # If the method was called with POST data, and the user is an admin,
    # it was called by a PaidForm. Handle that.
    if request.method == "POST":

        # Make a PaidForm from the POST data.
        form = forms.PaidForm(request.POST)

        # If the form is valid, get the right sponsorship, and change the amount paid to
        # whatever was in the form.
        if form.is_valid():
            relevant_sponsorship = get_object_or_404(Sponsorship, pk=form.cleaned_data['sponsorship_id'])
            relevant_sponsorship.amount_paid = form.cleaned_data['amount']
            relevant_sponsorship.save()

    # Get all the sponsorships in the system.
    sponsorships = Sponsorship.objects.order_by('sponsor__username')

    # Get all users, and use this to get a list of all email addresses.
    all_users = User.objects.order_by('username')
    all_subscribed_users = all_users.filter(subscribed=True)
    all_emails = [user.email for user in all_subscribed_users]

    all_wagers = Wager.objects.order_by('sponsor')

    newsletter_users = User.objects.filter(subscribed=True)
    newsletter_emails = [user.email for user in newsletter_users]

    # Build a context from the sponsorships, users, emails and the PaidForm
    context = {
        'sponsorships': sponsorships,
        'all_users': all_users,
        'all_emails': all_emails,
        'all_wagers': all_wagers,
        'newsletter_emails': newsletter_emails,
        'form': forms.PaidForm,
    }

    # Render and return the page with the context.
    return render(request, 'Running/overview.html', context)


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
    # Then, create a run object for each workout that does not currently have a run object.
    if request.GET.has_key('code'):

        # Get the code from the GET data. This will allow us to get an access token.
        code = request.GET['code']

        # Create an instance of the healthgraph API.
        rk_auth_mgr = healthgraph.AuthManager(settings.RUNKEEPER_CLIENT_ID, 
                                        settings.RUNKEEPER_CLIENT_SECRET, 
                                        settings.APP_URL + reverse('Running.views.register_runkeeper', 
                                                                    kwargs={'runner_id': request.user.id})
                                        )

        # Get the access token using the code and the instance of the healthgraph API.
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

        # Request the workout data for the user using our new, shiny access token.
        r = requests.get('https://api.runkeeper.com/fitnessActivities', 
                            headers={'Authorization': 'Bearer %s' % request.user.access_token}
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
                              distance=item['total_distance']/1000, 
                              start_date=date, 
                              end_date=date, 
                              source="runkeeper", 
                              source_id=item['uri'])
                new_run.save()

        # Redirect to the profile page of the user with id runner_id.
        url = reverse('user_view', kwargs={'user_id': request.user.id})
        return HttpResponseRedirect(url)

    # If the user has no code, and no token associated with their account, we need to start the
    # authentication process from scratch. 
    else:

        # Create an instance of the healthgraph API.
        rk_auth_mgr = healthgraph.AuthManager(settings.RUNKEEPER_CLIENT_ID, 
                                              settings.RUNKEEPER_CLIENT_SECRET,
                                              settings.APP_URL + reverse('register_runkeeper', 
                                              kwargs={'runner_id': request.user.id}))

        # Get the uri that should be accessed to get the code, and redirect there.
        rk_auth_uri = rk_auth_mgr.get_login_url()
        return HttpResponseRedirect(rk_auth_uri)

