# coding: utf8

from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.translation import ugettext as _

from profile.models import User
from sponsorship.models import Sponsorship
from wagers.models import Wager
from runs.models import Run

from .forms import PaidForm


@cache_page(60 * 1)  # cache it for 1 minute
def info_widget(request):
    all_users = User.objects.all()

    num_runners = len([us.id for us in all_users if us.is_runner])
    num_sponsors = len([us.id for us in all_users if us.is_sponsor])

    spships = Sponsorship.objects.all()
    amount_donated = sum([sp.amount_paid for sp in spships])

    wagers = Wager.objects.filter(status='paid')
    amount_donated += sum([wager.amount for wager in wagers])

    total_distance = Run.objects.all().aggregate(x=Sum('distance'))['x'] or 0

    context = {
        'num_runners': num_runners,
        'num_sponsors': num_sponsors,
        'amount_donated': amount_donated,
        'total_distance': total_distance,
    }
    return render(request, 'tools/info_widget.html', context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def charge_users_now(request):
    from payments.tasks import charge_users
    charge_users()
    messages.success(request, "all users have been charged!")
    return redirect('profile:my_page')

@user_passes_test(lambda u: u.is_staff)
@login_required
def overview(request):
    form = PaidForm()

    if request.method == "POST":
        form = PaidForm(request.POST)
        # If the form is valid, get the right sponsorship,
        # and change the amount paid to whatever was in the form.
        if form.is_valid():
            sponsorship_id = form.cleaned_data['sponsorship_id']
            relevant_sponsorship = get_object_or_404(Sponsorship,
                                                     id=sponsorship_id)
            relevant_sponsorship.amount_paid = form.cleaned_data['amount']
            relevant_sponsorship.save()
            messages.success(request, _("sponsorship has been changed"))

    sponsorships = Sponsorship.objects.order_by('sponsor__username')
    all_users = User.objects.order_by('username')
    all_subscribed_users = all_users.filter(subscribed=True)
    all_emails = [user.email for user in all_subscribed_users]
    all_wagers = Wager.objects.order_by('sponsor')
    newsletter_users = User.objects.filter(subscribed=True)
    newsletter_emails = [user.email for user in newsletter_users]

    context = {
        'sponsorships': sponsorships,
        'all_users': all_users,
        'all_emails': all_emails,
        'all_wagers': all_wagers,
        'newsletter_emails': newsletter_emails,
        'form': form,
    }
    return render(request, 'tools/overview.html', context)

