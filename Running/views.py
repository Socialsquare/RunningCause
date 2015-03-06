from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from Running.models import Sponsorship, Run, User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from django.utils import timezone
from allauth.account.forms import LoginForm, SignupForm
import datetime
from dateutil.relativedelta import relativedelta
import requests
from Running import forms
import time
import healthgraph
import json
from django.conf import settings
from django.core.mail import send_mail
from django.template import RequestContext, loader, Context, Template





# The main homepage. Displays a list of all users.
def home(request):

    print request.LANGUAGE_CODE
    # If a redirect URL has been specificed, that is what we should be showing
    # the user. Redirect there.
    if 'redirect' in request.session:
        return HttpResponseRedirect(request.session.pop('redirect'))

    # Otherwise, get a list of all users, sorted by their username.
    user_list = User.objects.order_by('username')

    # Create the context, using the user if authenticated.
    if request.user.is_authenticated():
        context = {'user_list': user_list,
            'user': request.user,
        }
    else:
        context = {'user_list': user_list,
            'user': False,
        }

    return render(request, 'Running/home.html', context)

# Shows a page for a specific user, displaying their username and all their sponsorships.
def user(request, user_id):

    print request.META['HTTP_HOST']
    # Get the user, or 404 if you can't find them.
    user = get_object_or_404(User, pk=user_id)

    # Get all of the user's recieved sponorships.
    # Then, calculate the total amount earned by adding the amount earned for each sponsorship
    # recieved.
    sponsorships = user.sponsorships_recieved.exclude(sponsor=None)
    amount_earned = 0
    for sponsorship in sponsorships:
        amount_earned = amount_earned + sponsorship.total_amount

    # Get all of the user's given sponsorships.
    # Then, calculate the total amount donated by adding the amount donated for each sponsorship
    # given.
    sponsorships_given = user.sponsorships_given.exclude(sponsor=None)
    amount_given = 0
    for sponsorship in sponsorships_given:
        amount_given = amount_given + sponsorship.total_amount

    # Get all the user's runs.
    # Then, calculate the total distance run by adding the distance run for each run.
    runs = user.runs.all()
    total_distance = 0
    for run in runs:
        total_distance = total_distance + run.distance

    # Default to saying that the user is not looking at their own page,
    # and is logged in. (As such, the accessor is "None", meaning they
    # get no special privileges in viewing the page)
    own_page = False
    accessor = None

    # If the user is authenticated, then set the accessor to be the user,
    # so that any special viewing priviledges can be figured out.
    # Then, figure out if the request is the viewer accessing their own page.
    # If it is, then set "own_page" to true.
    if request.user.is_authenticated():
        auth_user_id = request.user.id
        accessor = get_object_or_404(User, pk=auth_user_id)
        own_page = (str(auth_user_id) == str(user_id))
            
    # Build the context from the variables we've just set.
    context = {'user': user,
                'sponsorships': sponsorships,
                'sponsorships_given': sponsorships_given,
                'amount_earned':amount_earned,
                'amount_given':amount_given,
                'total_distance':total_distance,
                'accessor': accessor,
                'runs': runs,
                'own_page': own_page,
                'is_runner': user.is_runner,
                'is_sponsor': user.is_sponsor
                }

    # Render and return the page based on the context.
    return render(request, 'Running/user.html', context)

# When called with correct authorization, makes the profile of the user 
# with user id user_id public.
def make_user_public(request, user_id):
    # Verify that the user is logged in.
    if request.user.is_authenticated():

        # Verify that the user is logged in as the person whose profile
        # they're trying to make public.
        if int(request.user.id) == int(user_id):

            # If so, change the user with user id user_id to be public.
            user = get_object_or_404(User, pk=user_id)
            user.is_public = True
            user.save()

    # Regardless of whatever else happened, get the url of the profile
    # page for the user whose profile was requested to be made public,
    # and redirect there.
    url = reverse('Running.views.user', kwargs={'user_id': user_id})
    return HttpResponseRedirect(url)

# When called with correct authorization, makes the profile of the user 
# with user id user_id private.
def make_user_private(request, user_id):
    # Verify that the user is logged in.
    if request.user.is_authenticated():

        # Verify that the user is logged in as the person whose profile
        # they're trying to make private.
        if int(request.user.id) == int(user_id):

            # If so, change the user with user id user_id to be private.
            user = get_object_or_404(User, pk=user_id)
            user.is_public = False
            user.save()


    # Regardless of whatever else happened, get the url of the profile
    # page for the user whose profile was requested to be made private,
    # and rediect there.        
    url = reverse('Running.views.user', kwargs={'user_id': user_id})
    return HttpResponseRedirect(url)


# Takes the user to a page where they can either sign up or log in.
def signup_or_login(request):

    # Build the context containing the relevant forms.
    context = {'form':LoginForm,
                'signup_form':SignupForm}

    # Render and return the page with the context. 
    return render(request, 'Running/signup_or_login.html', context)

# Display information on every sponsorship, but only if the user is
# a superuser. Additionally, handles PaidForm, which which allows the user 
# to enter how much money has been paid from a sponsorship, making it easier to
# manually keep track of who owes what.
def overview(request):
    # If the method was called with POST data, and the user is an admin,
    # it was called by a PaidForm. Handle that.
    if request.method == "POST" and request.user.is_staff:

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
    all_emails = [user.email for user in all_users]

    # Build a context from the sponsorships, users, emails and the PaidForm
    context = {'sponsorships': sponsorships,
                'all_users': all_users,
                'all_emails': all_emails,
                'form': forms.PaidForm,
                }

    # Render and return the page with the context.
    return render(request, 'Running/overview.html', context)

# If called with correct authorization, delete the sponsorship with id sponsorship_ip.
def end_sponsorship(request, sponsorship_id, runner_id):
    # Verify that the user is authenticated.
    if request.user.is_authenticated():

        # Get the user that the accessor is currently logged in as, and the sponsorship
        # with id sponsorship_id.
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        sponsorship = get_object_or_404(Sponsorship, pk=sponsorship_id)

        # If the accessor is logged in as either the giver or reciever of the sponsorship,
        # set the sponsorship's end date to today.
        if user == sponsorship.sponsor or user == sponsorship.runner:
            sponsorship.end_date = datetime.date.today()
            sponsorship.save()

    # Regardless of what happened, redirect to the profile page of the user with id runner_id.
    url = reverse('Running.views.user', kwargs={'user_id': runner_id})
    return HttpResponseRedirect(url)

# Overall, update the runs of the users to reflect their runkeeper account. This can take a few forms.
#   -   If they haven't previously registered with runkeeper, request an access code through the healthgraph
#       api. Have runkeeper redirect to this url, so that we can have the possibility below.
#   -   If they haven't previously registered with runkeeper, but the request has a value 'code' in the GET
#       data, the first possibilty has been called, and has returned to this. User this code to get an
#       access token for the user, save it with the user, and call this method again to actually deal
#       with the workout data.
#   -   If the user accesses this url with a runkeeper token, our job is much easier. Just access this token,
#       use it to get all the workout data for the user, and use create new run objects for each workout 
#       that does not currently have a run object.
def register_runkeeper(request, runner_id):

    # Get the user with id runner_id.
    user = get_object_or_404(User, pk=runner_id)

    # Verify that the accessor is currently logged in as the user that they're trying to register with runkeeper.
    # If they are not, render and return an error message. Note: due to the design of the site, users should never
    # be able to accidentally access this without being logged in as the user they're trying to register with
    # runkeeper. If this ends up being relevant, it is almost definitely something malicious going on. Or a user
    # incompetent to the point where it's actually impressive.
    if request.user.is_authenticated() and int(request.user.id) == user.id:

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
                                                                        kwargs={'runner_id': runner_id})
                                            )

            # Get the access token using the code and the instance of the healthgraph API.
            access_token = rk_auth_mgr.get_access_token(code)

            # Associate the token with the user, and save.
            user.access_token = access_token
            user.save()

            # Now that we've associated the token with the user, we're done with authentication.
            # Call this view again to finally deal with the workout data.
            reverse('Running.views.register_runkeeper', 
                        kwargs={'runner_id': runner_id})

        # This means that the user has registered with runkeeper before, and has an access token.
        # Use this to get the workouts for the user, and create and store new run objects for
        # every run that has not been previously registered with runkeeper.
        elif user.access_token != "":

            # Request the workout data for the user using our new, shiny access token.
            r = requests.get('https://api.runkeeper.com/fitnessActivities', 
                                headers={'Authorization': 'Bearer %s' % user.access_token}
                                )

            # Convert the workout data from JSON to make it easier to work with.
            data = r.json()

            # Get all runs that are associated with the user, and that came from runkeeper.
            # Compile all the of the source ids for them (the ids that were given to them
            # by their source, in this case runkeeper). This is important so that we make
            # sure that we don't register the same run multiple times.
            runkeeper_runs = user.runs.filter(source="runkeeper")
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
                    new_run = Run(runner=user, 
                                    distance=item['total_distance']/1000, 
                                    start_date=date, 
                                    end_date=date, 
                                    source="runkeeper", 
                                    source_id=item['uri'])
                    new_run.save()

            # Redirect to the profile page of the user with id runner_id.
            url = reverse('Running.views.user', kwargs={'user_id': runner_id})
            return HttpResponseRedirect(url)

        # If the user has no code, and no token associated with their account, we need to start the
        # authentication process from scratch. 
        else:

            # Create an instance of the healthgraph API.
            rk_auth_mgr = healthgraph.AuthManager(settings.RUNKEEPER_CLIENT_ID, 
                                                    settings.RUNKEEPER_CLIENT_SECRET,
                                                    settings.APP_URL + reverse('Running.views.register_runkeeper', 
                                                        kwargs={'runner_id': runner_id}))

            # Get the uri that should be accessed to get the code, and redirect there.
            rk_auth_uri = rk_auth_mgr.get_login_url()
            return HttpResponseRedirect(rk_auth_uri)

    # An error message for when the user is not logged as the person they are trying to register runs for.
    # Means that either they are malicious, or have somehow managed to defeat the design of the website.
    return HttpResponse("You are not the runner you're trying to register with runkeeper a run for! Please go to your own page and try again.")

# Create a sponsorship from the person currently logged in, to the user with id sponsee_id.
def sponsor(request, sponsee_id, sponsorship_id=None):

    # If this view was called with POST data, or the field 'form' in request.session,
    # then the data has already been filled out.
    if request.method == "POST" or 'form' in request.session:

        # Verify that the user is logged in.
        if request.user.is_authenticated():


            # If this view was called with POST data, make an instance of SponsorForm from
            # the data.
            if request.method == "POST":
                form = forms.SponsorForm(request.POST)
            
            # If this view was called with 'form' in the session data, make an instance of 
            #   SponsorForm from the data.
            else:
                form = forms.SponsorForm(request.session.pop('form'))

            # Get the user objects for the potential sponsor and sponsee.
            user_id = request.user.id
            sponsee=get_object_or_404(User, pk=sponsee_id)
            sponsor = get_object_or_404(User, pk=user_id)

            # If the form is valid, get the data from it, and then make a sponsorship
            # object from that data.
            if form.is_valid():
                rate = form.cleaned_data['rate']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                max_amount = form.cleaned_data['max_amount']
                sponsorship = Sponsorship(runner=sponsee, 
                                            sponsor=sponsor, 
                                            rate=rate,
                                            start_date=start_date, 
                                            end_date=end_date, 
                                            max_amount=max_amount)

                # Save the sponsorship.
                sponsorship.save()

                # Redirect to the profile page of the user with id sponsee_id.
                url = reverse('Running.views.user', kwargs={'user_id': sponsee_id})
                return HttpResponseRedirect(url)
        else:

            # If the user is not authenticated, save the data from their form and save
            # the url of the current view as 'redirect' in session.
            request.session['form'] = request.POST
            request.session['redirect'] = reverse('Running.views.sponsor', kwargs={'sponsee_id':sponsee_id})

            # Redirect to the signup or login view.
            url = reverse('Running.views.signup_or_login')
            return HttpResponseRedirect(url)

    # Have invite default to a value that will read as "False".
    invite = None

    # Create the variable form, if it hasn't already been created up above.
    if not 'form' in locals():
        form = forms.SponsorForm

    # If this view recieved a sponsorship id, then we are filling out an invitation. If the sponsorship
    # id is valid, start out the form with the values in that sponsorship, and set invitation to be true.
    if sponsorship_id:
        invite = get_object_or_404(Sponsorship, pk=sponsorship_id)
        form = forms.SponsorForm(instance=invite)

    # Get the user object for the sponsee.
    runner = get_object_or_404(User, pk=sponsee_id)

    # Create a context from all the variables we've collected.
    context = {'runner': runner,
                'form': form,
                'invite': invite,
                }
    # Render and return the page with the context.
    return render(request, 'Running/sponsorship.html', context)

# Invites a the user with id sponsor_id to sponsor the user that's currently logged in.
def invite_sponsor(request, sponsor_id=None):

    print sponsor_id


    # If this view was called with POST data, or the field 'form' in request.session,
    # then the data has already been filled out.
    if request.method == "POST" or 'form' in request.session:

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

                # Create the message of the text.
                message_text = "{0} has requested you as a sponsor on Masanga Runners! Click this to proceed: {1} \n\nFeel free to ignore this if you're not interested in sponsoring {0}.".format(request.user.username, 
                                                                                                                                                                                            request.build_absolute_uri(email_url))

                # Send the email, attaching an HTML version as well.
                send_mail('Sponsorship Invitation', 
                            message_text, 
                            'postmaster@appa4d174eb9b61497e90a286ddbbc6ef57.mailgun.org',
                            [email], 
                            fail_silently=False,
                            html_message = loader.get_template('Running/email.html').render(Context({'message': message_text, 'request': request})))

                # Redirect to the profile or the user with id user_id.
                if sponsor_id:
                    url = reverse('Running.views.user', kwargs={'user_id': sponsor_id})
                else:
                    url = reverse('Running.views.user', kwargs={'user_id': user_id})
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

# Allows a user with id runner_id to manually input a run they did.
def input_run(request, runner_id):

    # If there's POST data on the request, then the form is being returned.
    if request.method == "POST":

        # Get the object for the current user, and verify that the accessor is logged in as them.
        runner = get_object_or_404(User, pk=runner_id)
        if request.user.is_authenticated():
            user = request.user
            if int(user.id) == int(runner_id):

                # If they are, convert the POST data into a form, and check that it's valid.
                form = forms.RunInputForm(request.POST)
                if form.is_valid():

                    # Get the various variables for the run.
                    runner = user
                    distance = form.cleaned_data['distance']
                    start_date = form.cleaned_data['start_date']

                    # If there was an end date, this was a collection of runs. Set the end date appropriately,
                    # and make a run object from our data.
                    if form.cleaned_data['end_date'] != None:
                        end_date = form.cleaned_data['end_date']
                    
                    # Otherwise, it was a single run. Set the end data appropriately, and make a run object from
                    # our data.
                    else:
                        end_date = form.cleaned_data['start_date']
                    run = Run(runner=runner, distance=distance, start_date=start_date, end_date=end_date)

                    # Save our run, and then redirect to the profile of the user with id runner_id.
                    run.save()

                    # Get a list of all sponsorships the user has recieved that were active when the run
                    # happened, then get a list of all relevant sponsors and their emails from that.
                    relevant_sponsorships = user.sponsorships_recieved.filter(end_date__gte=end_date, 
                                                                            start_date__lte=start_date)
                    relevant_sponsors = list(set([sponsorship.sponsor for sponsorship in relevant_sponsorships]))
                    relevant_emails = [sponsor.email for sponsor in relevant_sponsors]

                    # Generate a message from the information of the run, and send it out to all the relevant
                    # sponsors.
                    message_text = "{0} has run a distance of {1}km!".format(user.username, 
                                                                                distance)
                    send_mail('Run Update', 
                                message_text, 
                                'postmaster@appa4d174eb9b61497e90a286ddbbc6ef57.mailgun.org',
                                relevant_emails, 
                                fail_silently=False,
                                html_message = loader.get_template('Running/email.html').render(Context({'message': message_text})))

                    # Redirect to the user's page.
                    url = reverse('Running.views.user', kwargs={'user_id': runner_id})
                    return HttpResponseRedirect(url)

    # If form has not already been created, create it.
    if not 'form' in locals():
        form = forms.RunInputForm

    # Get the object of the runner, and verify that they're logged in as the runner they're trying to enter runs for.
    runner = get_object_or_404(User, pk=runner_id)
    if request.user.is_authenticated():
        user = request.user
        if int(user.id) == int(runner_id):

            # If they are, make a context from our variables.
            context = {
                'runner': runner,
                'form': form
                }

            # Render the page with the context and return it.
            return render(request, 'Running/run_input.html', context)

    # Otherwise, return an error. Note: this should not be possible, so it would likely indicate malicious
    # activity, or the user breaking the website in some unexpected way.
    return HttpResponse("You are not the runner you're trying to input a run for! Please go to your own page and try again.")


# Allows a user to edit the details of a run they did.
def edit_run(request, run_id):

    # Get the run and runner objects.
    run = get_object_or_404(Run, pk=run_id)
    runner = run.runner

    # If POST data is included in the request, then the form has been filled out and we're processing it now.
    if request.method == 'POST':

        # Check that the user is authenticated first (If they've managed to access this, they probably are, but
        # check to make sure that attacks aren't completely trivial)
        if request.user.is_authenticated():
            user = request.user

            # Verify that the user is the same user that the run belongs to. Again, this shouldn't be an issue
            # in the normal flow of the website, but, without this, attacks are completely trivial.
            if int(user.id) == int(runner.id):

                # Create a form from the POST data, and tie it to our particular run.
                form = forms.RunInputForm(request.POST, instance=run)
                if form.is_valid():

                    # Edit the run with the new variables.
                    run.distance = form.cleaned_data['distance']
                    run.start_date = form.cleaned_data['start_date']
                    if form.cleaned_data['end_date'] and form.cleaned_data['end_date'] > form.cleaned_data['start_date']:
                        run.end_date = form.cleaned_data['end_date']
                    else:
                        run.end_date = form.cleaned_data['start_date']

                    # Save the run to save our changes.
                    run.save()

                    # Redirect the user to their profile page.
                    url = reverse('Running.views.user', kwargs={'user_id': user.id})
                    return HttpResponseRedirect(url)
    
    # If the user is not authenticated, or they are authenticated as a user that doesn't own the run,
    # redirect them to a page stating that there is an error. This page is ugly, but there should
    # be no way to access this in the normal flow of things.
    if not request.user.is_authenticated() or int(runner.id) != int(request.user.id):
        return HttpResponse("You are not logged in as the correct runner! Please go back and log in as the correct runner.")

    # Create a form from our specific run, and use this, along with the run, to create a context.
    run_to_edit = get_object_or_404(Run, pk=run_id)
    form = forms.RunInputForm(instance=run_to_edit)
    context = {
                'run': run,
                'form': form
                }

    # Render and return the run_edit template with the context.
    return render(request, 'Running/run_edit.html', context)
