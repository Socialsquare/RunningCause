from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from Running.models import Sponsorship, Run, Payment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from django.utils import timezone
from Running import forms



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
def user(request, runner_id):
    runner = get_object_or_404(User, pk=runner_id)
    sponsorships = Sponsorship.objects.filter(runner__pk=runner_id)
    runs = Run.objects.filter(runner__pk=runner_id)
    payments = Payment.objects.filter(sponsorship__runner__pk=runner_id)
    own_page = False
    if request.user.is_authenticated():
        user_id = request.user.id
        own_page = (str(runner_id) == str(user_id))
    context = {'user': runner,
                'sponsorships': sponsorships,
                'runs': runs,
                'payments': payments,
                'own_page': own_page
                }
    return render(request, 'Running/user.html', context)

def sponsor(request, sponsee_id):
    if request.method == "POST":
        user_id = None
        if request.user.is_authenticated():
            user_id = request.user.id
            sponsee=get_object_or_404(User, pk=sponsee_id)
            form = forms.SponsorForm(request.POST)
            if form.is_valid():
                sponsor = form.cleaned_data['sponsor_name']
                rate = form.cleaned_data['rate']
                email = form.cleaned_data['sponsor_email']
                end_date = form.cleaned_data['end_date']
                max_amount = form.cleaned_data['max_amount']
                sponsorship = Sponsorship(runner=sponsee, sponsor=sponsor, rate=rate, email=email, end_date=end_date, max_amount=max_amount)
                sponsorship.save()
                runs = Run.objects.filter(runner__pk=sponsee.id)
                amount = 0
                for run in runs:
                    if run.date <= sponsorship.end_date and run.date >= sponsorship.start_date:
                        amount += run.distance * sponsorship.rate
                payment = Payment(sponsorship=sponsorship, amount=amount)
                payment.save()
                sponsorship.payment = payment
                sponsorship.save()
                return HttpResponseRedirect('/runners/%s/profile' % sponsee_id)
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
                    sponsorships = Sponsorship.objects.filter(id=user.id)
                    for sponsorship in sponsorships:
                        if not sponsorship.past_end_date:
                            payments = Payment.objects.filter(sponsorship=sponsorship)
                            amount_owed = 0
                            for payment in payments:
                                if not payment.active:
                                    amount_owed = amount_owed + payment.amount
                            for payment in payments:
                                if payment.active:
                                    payment.amount = payment.amount + run.distance * payment.sponsorship.rate
                                    if payment.amount + amount_owed > payment.sponsorship.max_amount:
                                        payment.amount = payment.sponsorship.max_amount - amount_owed
                                        payment.sponsorship.active = False
                                        payment.sponsorship.save()
                                        payment.active = False
                                    payment.save()
                        else:
                            sponsorship.active = False
                            sponsorship.save()
                    return HttpResponseRedirect('/runners/%s/profile' % runner_id)
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

