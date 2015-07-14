# coding: utf8
import logging

import stripe
import mailchimp

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from allauth.account.forms import LoginForm, SignupForm

from .models import User


log = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


def users_list(request):
    user_list = get_user_model().objects.order_by('username')
    context = {
       'user_list': user_list,
    }
    return render(request, 'profile/users_list.html', context)


def user_raised(request, user_id):
    person = get_object_or_404(get_user_model(), id=user_id)
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
        'person': person,
        'tab_name': 'raised',
    }
    return render(request, 'profile/user_raised.html', context)


def user_donated(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    sponsorships_given = person.sponsorships_given.all().exclude(sponsor=None)
    amount_given = 0
    for sponsorship in sponsorships_given:
        amount_given = amount_given + sponsorship.total_amount

    wagers_given = person.wagers_given.exclude(sponsor=None)
    own_page = request.user.id == person.id

    context = {
        'sponsorships_given': sponsorships_given,
        'amount_given': amount_given,
        'wagers_given': wagers_given,
        'own_page': own_page,
        'person': person,
        'tab_name': 'donations',
    }
    return render(request, 'profile/user_donated.html', context)


@login_required
def sign_in_landing(request):
    user = request.user
    if user.newsletter:
        try:
            m = mailchimp.Mailchimp(settings.COURRIERS_MAILCHIMP_API_KEY)
            m.lists.subscribe(settings.COURRIERS_MAILCHIMP_LIST,
                              {'email': user.email})
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
        url = reverse('profile:credit_card_prompt')
        return HttpResponseRedirect(url)
    url = reverse('profile:home')
    return HttpResponseRedirect(url)


@login_required
def credit_card_prompt(request):
    ctx = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'email': request.user.email
    }
    return render(request, 'profile/credit_card_prompt.html', ctx)


@login_required
@csrf_exempt
def register_customer(request):
    token = request.POST['stripeToken']
    customer = stripe.Customer.create(source=token,
                                      description=request.user.username)
    request.user.stripe_customer_id = customer.id
    request.user.save()
    return render(request, 'profile/credit_card_success.html', {})


@login_required
def unsubscribe(request):
    user = request.user
    user.subscribed = False
    user.save()
    return render(request, 'profile/unsubscribed_success.html', {})


@login_required
def subscribe(request):
    user = request.user
    user.subscribed = True
    user.save()
    return render(request, 'profile/subscribed_success.html', {})


@login_required
def unregister_card(request):
    user = request.user
    user.stripe_customer_id = None
    user.save()
    return render(request, 'profile/deregister_success.html', {})


def user_page(request, user_id):
    """
    Redirects to a page for a specific user, displaying their username and all
    their sponsorships.
    """
    user = get_object_or_404(User, pk=user_id)
    if (request.user.is_authenticated() and
            int(user.id) == int(request.user.id)) or \
            user.is_public:
        url = reverse('runs:user_runs', kwargs={'user_id': user_id})
    else:
        url = reverse('profile:user_raised', kwargs={'user_id': user_id})
    return HttpResponseRedirect(url)


@login_required
def user_settings(request):
    return render(request, 'profile/user_settings.html', {})


@login_required
def my_page(request):
    url = reverse('profile:user_page', kwargs={'user_id': request.user.id})
    return HttpResponseRedirect(url)


@login_required
def make_profile_public(request):
    request.user.is_public = True
    request.user.save()
    messages.info(request, _("Your settings has been saved."))
    return redirect('profile:user_settings')


@login_required
def make_profile_private(request):
    request.user.is_public = False
    request.user.save()
    messages.info(request, _("Your settings has been saved."))
    return redirect('profile:user_settings')


def signup_or_login(request):
    context = {
        'form': LoginForm,
        'signup_form': SignupForm
    }
    return render(request, 'profile/signup_or_login.html', context)
