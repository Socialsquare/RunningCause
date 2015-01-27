from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from Running.models import Sponsorship, Run, User
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from django.utils import timezone
import datetime
import requests
from Running import forms
import time
import healthgraph
import json
from django.conf import settings
from django.core.mail import send_mail



# @login_required(login_url='/runners/account/login')

# The main homepage. Displays a list of all users.
def home(request):
    user_list = User.objects.order_by('-username')
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
    send_mail('HELLO!', 'TEST EMAIL.', 'from@example.com', ['niles_christensen@yahoo.com'], fail_silently=False)

    user = get_object_or_404(User, pk=user_id)
    sponsorships = user.sponsorships_recieved.all()
    sponsorships_given = user.sponsorships_given.all()
    runs = user.runs.all()
    own_page = False
    runkeeper = True
    accessor = None

    if request.user.is_authenticated():
        print "User is authenticated"
        auth_user_id = request.user.id
        accessor = get_object_or_404(User, pk=auth_user_id)
        print accessor
        own_page = (str(auth_user_id) == str(user_id))
        runkeeper = request.session.has_key('rk_access_token')
            
    context = {'user': user,
                'sponsorships': sponsorships,
                'sponsorships_given': sponsorships_given,
                'accessor': accessor,
                'runs': runs,
                'own_page': own_page,
                'runkeeper': runkeeper,
                'is_runner': user.is_runner,
                'is_sponsor': user.is_sponsor
                }

    print "Own page: %s" % context['own_page']

    return render(request, 'Running/user.html', context)

def end_sponsorship(request, sponsorship_id, runner_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        sponsorship = get_object_or_404(Sponsorship, pk=sponsorship_id)
        if user == sponsorship.sponsor or user == sponsorship.runner:
            sponsorship.end_date = datetime.date.today()
            sponsorship.save()
            url = reverse('Running.views.user', kwargs={'user_id': runner_id})
            return HttpResponseRedirect(url)

def register_runkeeper(request, runner_id):
    if request.GET.has_key('code'):
        code = request.GET['code']
        rk_auth_mgr = healthgraph.AuthManager(settings.RUNKEEPER_CLIENT_ID, 
                                        settings.RUNKEEPER_CLIENT_SECRET, 
                                        # request.build_absolute_uri(request.get_full_path()))
                                        # '127.0.0.1/register/runkeeper/')
                                        settings.APP_URL + reverse('Running.views.register_runkeeper', kwargs={'runner_id': runner_id}))


        user = get_object_or_404(User, pk=runner_id)
        access_token = rk_auth_mgr.get_access_token(code)
        user.access_token = access_token
        user.save()
        print access_token
        r = requests.get('https://api.runkeeper.com/fitnessActivities', headers={'Authorization': 'Bearer %s' % user.access_token})
        data = r.json()
        print data['items']
        for item in data['items']:
            print item['total_distance']
        runkeeper_runs = user.runs.filter(source="runkeeper")
        registered_ids = [run.source_id for run in runkeeper_runs]
        for item in data['items']:
            if item['uri'] not in registered_ids:
                date = time.strptime(item['start_time'][5:16], "%d %b %Y")
                date = datetime.datetime(*date[:6]).date()
                new_run = Run(runner=user, distance=item['total_distance']/1000, date=date, source="runkeeper", source_id=item['uri'])
                new_run.save()
                # send_mail('HELLO!', 'TEST EMAIL.', 'from@example.com', ['niles_christensen@yahoo.com'], fail_silently=False)
            # else:
            #     run = get_object_or_404(Run, pk=runner_id)
            #     run.save()
        # runkeeper_user = healthgraph.User(session=healthgraph.Session(user.access_token))
        # profile = runkeeper_user.get_profile()
        # # records = runkeeper_user.get_records()
        # act_iter = runkeeper_user.get_fitness_activity_iter()
        # # activities = [act_iter.next() for _ in xrange(act_iter.count()]
        # # print activities

        url = reverse('Running.views.user', kwargs={'user_id': runner_id})
        return HttpResponseRedirect(url)
    else:
        print request.build_absolute_uri(request.get_full_path())
        rk_auth_mgr = healthgraph.AuthManager(settings.RUNKEEPER_CLIENT_ID, 
                                                settings.RUNKEEPER_CLIENT_SECRET, 
                                                # request.build_absolute_uri(request.get_full_path()))
                                                # '127.0.0.1/register/runkeeper/')
                                                settings.APP_URL + reverse('Running.views.register_runkeeper', kwargs={'runner_id': runner_id}))

        rk_auth_uri = rk_auth_mgr.get_login_url()
        print "Getting code..."
        return HttpResponseRedirect(rk_auth_uri)


def sponsor(request, sponsee_id):
    if request.method == "POST":
        user_id = None
        if request.user.is_authenticated():
            user_id = request.user.id
            sponsee=get_object_or_404(User, pk=sponsee_id)
            sponsor = get_object_or_404(User, pk=user_id)
            form = forms.SponsorForm(request.POST)
            if form.is_valid():
                rate = form.cleaned_data['rate']
                end_date = form.cleaned_data['end_date']
                max_amount = form.cleaned_data['max_amount']
                sponsorship = Sponsorship(runner=sponsee, sponsor=sponsor, rate=rate, end_date=end_date, max_amount=max_amount)
                sponsorship.save()

                url = reverse('Running.views.user', kwargs={'user_id': sponsee_id})
                return HttpResponseRedirect(url)
            else:
                return HttpResponse("Hmm, something's wrong with that form.")
        return HttpResponse("You need to be logged in to do that")
    else:
        runner = get_object_or_404(User, pk=sponsee_id)
        context = {'runner': runner,
                'form': forms.SponsorForm,
        }
        return render(request, 'Running/sponsorship.html', context)

def input_run(request, runner_id):
    if request.method == "POST":
        runner = get_object_or_404(User, pk=runner_id)
        if request.user.is_authenticated():
            user = request.user
            if int(user.id) == int(runner_id):
                form = forms.RunInputForm(request.POST)
                if form.is_valid():
                    runner = user
                    distance = form.cleaned_data['distance']
                    date = form.cleaned_data['date']
                    run = Run(runner=runner, distance=distance, date=date)
                    run.save()
                    # sponsorships = Sponsorship.objects.filter(id=user.id)
                    # for sponsorship in sponsorships:
                    #     if not sponsorship.past_end_date:
                    #         payments = Payment.objects.filter(sponsorship=sponsorship)
                    #         amount_owed = 0
                    #         for payment in payments:
                    #             if not payment.active:
                    #                 amount_owed = amount_owed + payment.amount
                    #         for payment in payments:
                    #             if payment.active:
                    #                 payment.amount = payment.amount + run.distance * payment.sponsorship.rate
                    #                 if payment.amount + amount_owed > payment.sponsorship.max_amount:
                    #                     payment.amount = payment.sponsorship.max_amount - amount_owed
                    #                     payment.sponsorship.active = False
                    #                     payment.sponsorship.save()
                    #                     payment.active = False
                    #                 payment.save()
                    #     else:
                    #         sponsorship.active = False
                    #         sponsorship.save()
                    url = reverse('Running.views.user', kwargs={'user_id': runner_id})
                    return HttpResponseRedirect(url)
        return HttpResponse("Hmm, something went very wrong. Please try again.")
    else:
        runner = get_object_or_404(User, pk=runner_id)
        if request.user.is_authenticated():
            user = request.user
            if int(user.id) == int(runner_id):
                context = {'runner': runner,
                    'form': forms.RunInputForm
                }
                return render(request, 'Running/run_input.html', context)
        return HttpResponse("You are not the runner you're trying to input a run for! Please go to your own page and try again.")

