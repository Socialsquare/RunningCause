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


def home(request):
    if 'redirect' in request.session:
        return HttpResponseRedirect(request.session.pop('redirect'))
    user_list = User.objects.order_by('username')
    context = {
       'user_list': user_list,
    }
    return render(request, 'Running/home.html', context)



def user_raised(request, user_id):
    person = get_object_or_404(User, id=user_id)
    wager_form = forms.WagerForm
    sponsor_form = forms.SponsorForm
    invite_form = forms.EmailInviteForm

    if request.method == "POST":

        if not request.user.is_authenticated():
            messages.error(request, _("Please log-in"))
            return redirect('Running.views.signup_or_login')

        form_name = request.POST['form_name']
        if form_name == 'sponsor_form':
            sponsor_form = forms.SponsorForm(request.POST)
            if sponsor_form.is_valid():
                rate = sponsor_form.cleaned_data['rate']
                start_date = sponsor_form.cleaned_data['start_date']
                end_date = sponsor_form.cleaned_data['end_date']
                max_amount = sponsor_form.cleaned_data['max_amount']
                sponsorship = Sponsorship(
                    runner=person,
                    sponsor=request.user,
                    rate=rate,
                    start_date=start_date,
                    end_date=end_date,
                    max_amount=max_amount
                )
                sponsorship.save()
                return redirect('signup_or_login')

        elif form_name == 'wager_form':

        elif form_name == 'invite_form':



    sponsorships = person.sponsorships_recieved.exclude(sponsor=None)
    amount_earned = 0
    for sponsorship in sponsorships:
        amount_earned = amount_earned + sponsorship.total_amount

    wagers_recieved = person.wagers_recieved.exclude(sponsor=None)

    own_page = False
    if request.user.is_authenticated():
        own_page = request.user.id == person.id

    context = {
        'sponsorships': sponsorships,
        'amount_earned': amount_earned,
        'wagers_recieved': wagers_recieved,
        'own_page': own_page,
        'sponsor_form': sponsor_form,
        'wager_form': wager_form,
        'invite_form': invite_form,
        'person': person,
        'tab_name': 'raised',
    }
    return render(request, 'Running/user_raised.html', context)


def user_donated(request, user_id):
    person = get_object_or_404(User, pk=user_id)
    invite_form = forms.InviteForm
    wager_form = forms.InviteWagerForm

    if request.method == "POST":
        if not request.user.is_authenticated():
            messages.error(_("Please log-in"))
            return redirect('signup_or_login')
        form_name = request.POST['form_name']
        if form_name == 'invite_form':
            invite_form = forms.InviteForm(request.POST)

            if invite_form.is_valid():
                sponsee = request.user
                sponsor = person
                email = sponsor.email

                rate = invite_form.cleaned_data['rate']
                start_date = invite_form.cleaned_data['start_date']
                end_date = invite_form.cleaned_data['end_date']
                max_amount = invite_form.cleaned_data['max_amount']
                sponsorship = Sponsorship(runner=sponsee,
                                          sponsor=None,
                                          rate=rate,
                                          start_date=start_date,
                                          end_date=end_date,
                                          max_amount=max_amount)
                sponsorship.save()
                email_url = reverse('sponsor_from_invite',
                                    kwargs={'sponsee_id': sponsee.id,
                                            'sponsorship_id':sponsorship.id})
                email_url = reverse('sponsor_from_invite',
                                    kwargs={'sponsee_id': sponsee.id,
                                            'sponsorship_id':sponsorship.id})
                full_email_url = request.build_absolute_uri(email_url)

                ctx = {
                    'runner': sponsee.username, 
                    'link': full_email_url, 
                    'BASE_URL': settings.BASE_URL, 
                    'title': 'Masanga Runners sponsorinvitation'
                }
                html_msg = loader.get_template('Email/email_invite.html')\
                    .render(Context(ctx))
                send_mail('Masanga Runners sponsorinvitation',
                          "",
                          settings.DEFAULT_FROM_EMAIL,
                          [email, ],
                          fail_silently=True,
                          html_message=html_msg)

                return redirect('user_donated', user_id=user_id)

        elif form_name == 'wager_form':
            wager_form = forms.InviteWagerForm(request.POST)
            if wager_form.is_valid():
                sponsee = get_object_or_404(User, pk=request.user.id)
                sponsor = person
                email = sponsor.email
                amount = wager_form.cleaned_data['amount']
                remind_date = wager_form.cleaned_data['remind_date']
                wager_text = wager_form.cleaned_data['wager_text']
                wager = Wager(runner=sponsee,
                              sponsor=None,
                              amount=amount,
                              remind_date=remind_date,
                              wager_text=wager_text)
                wager.save()
                email_url = reverse('wager_from_invite',
                                    kwargs={'sponsee_id': sponsee.id,
                                            'wager_id': wager.id})
                full_link = request.build_absolute_uri(email_url)

                ctx = {
                    'runner': sponsee.username,
                    'link': full_link,
                }
                tmpl = loader.get_template('Email/wager_request.html')
                html_msg = tmpl.render(Context(ctx))
                send_mail('Masanga Runners invitation til væddemål',
                          '',
                          settings.DEFAULT_FROM_EMAIL,
                          [email, ],
                          fail_silently=True,
                          html_message=html_msg)

    sponsorships_given = person.sponsorships_given.all().exclude(sponsor=None)
    amount_given = 0
    for sponsorship in sponsorships_given:
        amount_given = amount_given + sponsorship.total_amount

    wagers_given = person.wagers_given.exclude(sponsor=None)
    accessor = None
    own_page = request.user.id == person.id

    context = {
        'sponsorships_given': sponsorships_given,
        'amount_given': amount_given,
        'wagers_given': wagers_given,
        'own_page': own_page,
        'invite_form': invite_form,
        'wager_form': wager_form,
        'person': person,
        'tab_name': 'donations',
    }
    return render(request, 'Running/user_donated.html', context)


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
    context = {'sponsorships': sponsorships,
                'all_users': all_users,
                'all_emails': all_emails,
                'all_wagers': all_wagers,
                'newsletter_emails': newsletter_emails,
                'form': forms.PaidForm,
                }

    # Render and return the page with the context.
    return render(request, 'Running/overview.html', context)


@login_required
def end_sponsorship(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorship, pk=sponsorship_id)

    if request.user == sponsorship.sponsor or \
            request.user == sponsorship.runner:
        sponsorship.end_date = datetime.date.today()
        sponsorship.save()
        messages.success(request, _("Sponsorship has been ended."))
        return redirect('Running.views.user_donated', user_id=request.user.id)

    messages.error(request,
                   _("You are not a associated with this sponsorship."))
    return redirect('my_page')


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


@login_required
def add_sponsorship(request, runner_id):
    """
    Create a sponsorship from a person currently logged in(sponsor),
    to a runner with given runner_id (user id).
    """
    runner = get_object_or_404(User, pk=runner_id)
    sponsor = request.user
    form = forms.SponsorForm
    if request.method == "POST":
        form = forms.SponsorForm(request.POST)
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
            url = reverse('user_donated', kwargs={'user_id': sponsor.id})
            return HttpResponseRedirect(url)

    context = {
        'runner': runner,
        'form': form,
    }
    return render(request, 'Running/sponsorship.html', context)


@login_required
def invite_sponsor(request, sponsor_id=None):
    if request.method == "POST":

        # Verify that the user is logged in.
        if request.user.is_authenticated():

            # If this view was called with POST data, make an instance of SponsorForm from
            # the data.
            if request.method == 'POST':
                if sponsor_id:
                    form = forms.InviteForm(request.POST)
                else:
                    form = forms.EmailInviteForm(request.POST)

            # If this view was called with 'form' in the session data, make an instance of 
            # SponsorForm from the data.
            else:
                form = forms.InviteForm(request.session.pop('form'))


            # If the form is valid, get the data from it, and then make a sponsorship
            # object from that data. Notably, make sure that the sponsor is None.
            # This will prevent it from being confused with an actual sponsorship.
            # If the potential sponsor accepts, a new sponsorship will be made,
            # listing them as the sponsor.
            if form.is_valid():

                # Get the user objects for the potential sponsor and sponsee.
                user_id = request.user.id
                sponsee = get_object_or_404(User, pk=user_id)
                if sponsor_id:
                    sponsor = get_object_or_404(User, pk=sponsor_id)
                    email = sponsor.email
                else:
                    email = form.cleaned_data['email']
                

                rate = form.cleaned_data['rate']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                max_amount = form.cleaned_data['max_amount']
                sponsorship = Sponsorship(runner=sponsee, 
                                            sponsor=None, 
                                            rate=rate, 
                                            start_date=start_date,
                                            end_date=end_date,
                                            max_amount=max_amount)

                # If the sponsorship is to be for a single day, then make it so that
                # the sponsorship starts on what was originally end_date, and ends
                # the next day.                
                # if form.cleaned_data['single_day']:
                #     sponsorship.start_date = sponsorship.end_date
                #     sponsorship.end_date = sponsorship.end_date + relativedelta(days=1)

                # Save the sponsorship.
                sponsorship.save()

                # Now begins the process of emailing the potential sponsor!

                # First, get the link that the potential sponsor will be presented with,
                # and can follow to sponsor the potential sponsee.
                email_url = reverse('sponsor_from_invite', kwargs={'sponsee_id': sponsee.id,
                                                                    'sponsorship_id':sponsorship.id})

                full_email_url = request.build_absolute_uri(email_url)

                # Send the email, attaching an HTML version as well.
                send_mail('Masanga Runners sponsorinvitation', 
                            "", 
                            settings.DEFAULT_FROM_EMAIL,
                            [email], 
                            fail_silently=True,
                            html_message = loader.get_template('Email/email_invite.html').render(Context({'runner': sponsee.username, 'link': full_email_url, 'domain': settings.BASE_URL, 'title': 'Masanga Runners sponsorinvitation'})))


                # Redirect to the profile or the user with id user_id.
                if sponsor_id:
                    url = reverse('Running.views.user_view', kwargs={'user_id': sponsor_id})
                else:
                    url = reverse('Running.views.user_view', kwargs={'user_id': user_id})
                return HttpResponseRedirect(url)

        else:

            # If the user is not authenticated, save the data from their form and save
            # the url of the current view as 'redirect' in session.
            request.session['form'] = request.POST
            request.session['redirect'] = reverse('Running.views.invite_sponsor', kwargs={'sponsor_id':sponsor_id})

            # Redirect to the signup or login view.
            url = reverse('Running.views.signup_or_login')
            return HttpResponseRedirect(url)

    # Otherwise, prepare the page with the sponsorship form for the user.
    # Get the user object, then create an instance of form if it hasn't already been created.
    if sponsor_id:
        sponsor = get_object_or_404(User, pk=sponsor_id)
    else:
        sponsor = None
    if 'form' not in locals():
        if sponsor_id:
            form = forms.InviteForm
        else:
            form = forms.EmailInviteForm

    # Use our variables to make a context.
    context = {'sponsor': sponsor,
                'form': form
                }

    # Render the page with the context and return it.
    return render(request, 'Running/invite.html', context)




