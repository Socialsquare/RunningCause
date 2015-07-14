# coding: utf8
import logging


from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, Context
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from .models import Wager
from .forms import WagerForm, WagerUpdateForm, InviteWagerForm
from django.http.response import HttpResponseForbidden


log = logging.getLogger(__name__)


@login_required
def make_wager(request, sponsee_id, wager_id=None):
    """
    Create a wager from the person currently logged in,
    to the user with id sponsee_id.
    """
    form = WagerForm
    if request.method == "POST":
        form = WagerForm(request.POST)
        user_id = request.user.id
        sponsee = get_object_or_404(get_user_model(), pk=sponsee_id)
        sponsor = get_object_or_404(get_user_model(), pk=user_id)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            remind_date = form.cleaned_data['remind_date']
            wager_text = form.cleaned_data['wager_text']

            wager = Wager(runner=sponsee,
                          sponsor=sponsor,
                          amount=amount,
                          remind_date=remind_date,
                          wager_text=wager_text)

            if wager_id:
                old_wager = get_object_or_404(Wager, id=wager_id)
                old_wager.delete()
            wager.save()

            link = reverse('profile:user_donated',
                           kwargs={'user_id': sponsor.id})
            full_link = request.build_absolute_uri(link)
            subject = _('Masanga Runners wagering notification')
            ctx = {
                'sponsor': sponsor.username,
                'link': full_link,
            }
            tmpl = 'wagers/email/wager_challenged.html'
            html_msg = loader.get_template(tmpl)\
                .render(Context(ctx))
            send_mail(subject,
                      '',
                      settings.DEFAULT_FROM_EMAIL,
                      [sponsee.email],
                      fail_silently=True,
                      html_message=html_msg
                      )
            return redirect('profile:user_page', user_id=sponsee_id)
    invite = None

    # If this view recieved a sponsorship id, then we are filling out an invitation. If the sponsorship
    # id is valid, start out the form with the values in that sponsorship, and
    # set invitation to be true.
    if wager_id:
        invite = get_object_or_404(Wager, pk=wager_id)
        form = WagerForm(instance=invite)

    runner = get_object_or_404(get_user_model(), pk=sponsee_id)

    context = {
        'runner': runner,
        'form': form,
        'invite': invite,
    }
    return render(request, 'Running/wager.html', context)

"""
            wager_form = forms.WagerForm(request.POST)
            if wager_form.is_valid():
                amount = wager_form.cleaned_data['amount']
                remind_date = wager_form.cleaned_data['remind_date']
                wager_text = wager_form.cleaned_data['wager_text']
                wager = Wager(runner=person,
                              sponsor=request.user,
                              amount=amount,
                              remind_date=remind_date,
                              wager_text=wager_text)
                wager.save()

                link = reverse('user_donated',
                               kwargs={'user_id': person.id})
                full_link = request.build_absolute_uri(link)
                ctx = {
                    'sponsor': person.username,
                    'link': full_link,
                }
                tname = 'Email/wager_challenged.html'
                tmpl = loader.get_template(tname)
                html_msg = tmpl.render(Context(ctx))
                # FIXME: task!
                send_mail('Masanga Runners væddemåls-notifikation',
                          '',
                          settings.DEFAULT_FROM_EMAIL,
                          [person.email, ],
                          fail_silently=True,
                          html_message=html_msg)
"""


@login_required
def invite_wager(request, sponsor_id):
    """
    Invites a the user with id sponsor_id to sponsor the user that's
    currently logged in.
    """

    sponsor = get_object_or_404(get_user_model(), pk=sponsor_id)
    form = InviteWagerForm()
    if request.method == "POST":
        form = InviteWagerForm(request.POST)
        if form.is_valid():
            sponsee = request.user
            email = sponsor.email
            amount = form.cleaned_data['amount']
            remind_date = form.cleaned_data['remind_date']
            wager_text = form.cleaned_data['wager_text']
            wager = Wager(runner=sponsee,
                          sponsor=None,
                          amount=amount,
                          remind_date=remind_date,
                          wager_text=wager_text)

            wager.save()
            email_url = reverse('wagers:wager_from_invite',
                                kwargs={'sponsee_id': sponsee.id,
                                        'wager_id': wager.id})
            full_link = request.build_absolute_uri(email_url)
            send_mail('Masanga Runners invitation til væddemål',
                      '',
                      settings.DEFAULT_FROM_EMAIL,
                      [email],
                      fail_silently=True,
                      html_message=loader.get_template('wagers/email/wager_request.html').render(Context({'runner': sponsee.username,
                                                                                                   'link': full_link,
                                                                                                   'request': request})))

            return redirect('profile:user_page', user_id=sponsor_id)
    context = {
        'sponsor': sponsor,
        'form': form
    }
    return render(request, 'wagers/wager_invite.html', context)


@login_required
def update_wager(request, wager_id):
    wager = get_object_or_404(Wager, pk=wager_id)
    form = WagerUpdateForm()

    if request.method == "POST":
        if int(request.user.id) == int(wager.runner.id):

            form = WagerUpdateForm(request.POST)

            if form.is_valid():
                update_text = form.cleaned_data['update_text']
                wager.update_text = update_text
                wager.save()
                return render(request, 'wagers/wager_update_success.html', {})

        else:
            return HttpResponseForbidden("You are not the user who recieved "
                                         "the wager! You cannot update "
                                         "this wager.")
    context = {
        'wager': wager,
        'form': form
    }
    return render(request, 'wagers/wager_update.html', context)


@login_required
def confirm_wager(request, wager_id):
    wager = get_object_or_404(Wager, pk=wager_id)
    if request.user.id == wager.sponsor.id:
        wager.fulfilled = True
        wager.save()
        return render(request, 'Running/wager_confirm_success.html', {})
    return HttpResponseForbidden("You are not the user who gave "
                                 "the wager! You cannot confirm "
                                 "this wager.")


@login_required
def decline_wager(request, wager_id):
    wager = get_object_or_404(Wager, pk=wager_id)
    if request.user.id == wager.sponsor.id:
        wager.delete()
        return render(request, 'Running/wager_deny_success.html', {})
    return HttpResponseForbidden("You are not the user who gave the wager! "
                                 "You cannot decline this wager.")
