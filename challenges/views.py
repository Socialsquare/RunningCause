# coding: utf8
"""
Challenge is a type of a challenge.
* A runner can invite a sponsor to a challenge, runner challenge itself and asks
  for sponsorship.
* A sponsor can challenge a runner by sending him a challenge.

"""

import json
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.db import transaction

from .models import Challenge, ChallengeRequest
from .forms import ChallengeForm, ChallengeFeedbackForm, ChallengeChallengePreviewForm
from django.http.response import HttpResponseForbidden, HttpResponseNotFound,\
    HttpResponseRedirect


log = logging.getLogger(__name__)


@login_required
def challenge_runner(request, person_id):
    """
    Sponsor creates a challenge for a runner with person_id.
    """
    sponsor = request.user
    runner = get_object_or_404(get_user_model(), pk=person_id)
    if runner == sponsor:
        return HttpResponseForbidden()

    form = ChallengeForm()
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            proposed_challenge = json.dumps({
                'amount': form.cleaned_data['amount'],
                'end_date': form.cleaned_data['end_date'],
                'challenge_text': form.cleaned_data['challenge_text'],
                }, cls=DjangoJSONEncoder)

            challenge_req = ChallengeRequest.objects.create(runner=runner,
                sponsor=sponsor, proposed_challenge=proposed_challenge)

            link = reverse('challenges:preview_challenge',
                           kwargs={'token': challenge_req.token})
            full_link = request.build_absolute_uri(link)
            subject = _('%(username)s has challenged you') % {
                'username': sponsor.username
            }
            ctx = {
                'sponsor': sponsor.username,
                'link': full_link,
                'BASE_URL': settings.BASE_URL,
            }
            tmpl = 'challenges/emails/challenge_runner.html'
            html_msg = loader.get_template(tmpl)\
                .render(Context(ctx))
            send_mail(
                subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [runner.email],
                fail_silently=True,
                html_message=html_msg
            )
            msg = _("You have just challenge %(username)s") % {
                'username': runner.username
            }
            messages.info(request, msg)
            return redirect('profile:user_page', user_id=runner.id)

    context = {
        'runner': runner,
        'form': form,
    }
    return render(request, 'challenges/challenge_runner.html', context)


@login_required
def invite_sponsor_to_challenge(request, person_id=None):
    """
    Invites a user with person_id to sponsor a challenge for the user
    currently logged in.
    """
    runner = request.user
    sponsor = get_object_or_404(get_user_model(), pk=person_id)
    if runner == sponsor:
        return HttpResponseForbidden()

    form = ChallengeForm()
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            proposed_challenge = json.dumps({
                'amount': form.cleaned_data['amount'],
                'end_date': form.cleaned_data['end_date'],
                'challenge_text': form.cleaned_data['challenge_text'],
                }, cls=DjangoJSONEncoder)

            challenge_req = ChallengeRequest.objects.create(runner=runner,
                sponsor=sponsor, proposed_challenge=proposed_challenge)

            email_url = reverse('challenges:preview_invitation_challenge',
                                kwargs={'token': challenge_req.token.hex})
            full_link = request.build_absolute_uri(email_url)
            ctx = {
                'runner': runner.username,
                'link': full_link,
                'challenge_text': form.cleaned_data['challenge_text'],
                'BASE_URL': settings.BASE_URL
            }
            tmpl = 'challenges/emails/invite_sponsor_to_challenge.html'
            html_msg = loader.get_template(tmpl)\
                .render(Context(ctx))
            send_mail(_('Masanga Runners invitation to challenge'),
                      '',
                      settings.DEFAULT_FROM_EMAIL,
                      [sponsor.email],
                      fail_silently=False,
                      html_message=html_msg)

            messages.info(request, _("You have send invitation"
                                     " to %(username)s to challenge you.") %\
                          dict(username=challenge_req.sponsor.username))
            return redirect('profile:user_page', user_id=sponsor.id)
    context = {
        'person': sponsor,
        'form': form
    }
    return render(request, 'challenges/invite_sponsor_to_challenge.html', context)


class FeedbackChallenge(View):
    http_method_names = ['get', 'post']
    template_name = 'challenges/feedback_challenge.html'
    form_class = ChallengeFeedbackForm

    def _check_challenge_permission(self, challenge):
        if self.request.user not in [challenge.sponsor, challenge.runner]:
            raise PermissionDenied("You cannot update this challenge.")

        if self.request.user == challenge.runner and \
                challenge.status != Challenge.ACTIVE:
                raise PermissionDenied("Challenge has already been completed.")

        if self.request.user == challenge.sponsor and \
                challenge.status != Challenge.COMPLETED:
            raise PermissionDenied("Challenge is not completed yet.")

    def get(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        self._check_challenge_permission(challenge)
        form = self.form_class()
        ctx = {
            'challenge': challenge,
            'form': form,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        self._check_challenge_permission(challenge)

        form = self.form_class(request.POST)
        if form.is_valid():
            feedback_msg = form.cleaned_data['feedback_msg']
            action = request.POST.get('action')
            if request.user == challenge.runner:
                challenge.runner_msg = feedback_msg
                if action == 'success':
                    challenge.status = Challenge.COMPLETED
                    msg = _("Congratulations!, Your update will be send to "
                            "the sponsor for the final review.")
                    email_subject = _("%(runner)s completed the "
                                      "challenge successfully!") % {
                        'runner': challenge.runner.username
                    }
                    email_template = 'challenges/emails/challenge_success.html'
                    email_link = reverse('challenges:feedback_challenge',
                                         kwargs={'challenge_id': challenge.id})
                else:
                    challenge.status = Challenge.DECLINED
                    msg = _("Too bad. Your sponsor will be notified about the "
                            "failed challenge.")
                    email_subject = _("%(runner)s failed to complete the "
                                      "challenge!") % {
                        'runner': challenge.runner.username
                    }
                    email_template = 'challenges/emails/challenge_failure.html'
                    email_link = reverse('challenges:challenge_runner',
                                         kwargs={
                                            'person_id': challenge.runner.id
                                         })

                absolute_link = request.build_absolute_uri(email_link)
                ctx = Context({
                    'runner': challenge.runner.username,
                    'challenge_text': challenge.challenge_text,
                    'runners_message': challenge.runner_msg,
                    'link': absolute_link,
                    'BASE_URL': settings.BASE_URL,
                })
                email_msg = loader.get_template(email_template).render(ctx)
                send_mail(email_subject,
                          '',
                          settings.DEFAULT_FROM_EMAIL,
                          [challenge.sponsor.email, ],
                          html_message=email_msg)

                redirect_url = reverse('profile:user_raised',
                                       kwargs=dict(user_id=request.user.id))
            elif request.user == challenge.sponsor:
                challenge.sponsor_msg = feedback_msg
                redirect_url = reverse('profile:user_donated',
                                       kwargs=dict(user_id=request.user.id))
                if action == 'confirm':
                    challenge.status = Challenge.CONFIRMED
                    msg = _("You have accepted to pay for the challenge. "
                            "The money will be charged at the end of the "
                            "quarter.")
                else:  # request.POST.get('submit') == 'decline':
                    challenge.status = Challenge.DECLINED
                    msg = _("You have declined to pay for the challenge.")
            challenge.save()
            messages.info(request, msg)
            return HttpResponseRedirect(redirect_url)

        ctx = {
            'challenge': challenge,
            'form': form
        }
        return render(request, self.template_name, ctx)
feedback_challenge = login_required(FeedbackChallenge.as_view())


@login_required
def preview_challenge(request, token=None):
    """
    Runner can either accept or reject the challenge.
    """
    challenge_req = ChallengeRequest.objects.get(token=token)
    if challenge_req.runner != request.user or\
            challenge_req.status != ChallengeRequest.NEW:
        return HttpResponseForbidden()

    proposed = json.loads(challenge_req.proposed_challenge)
    form = ChallengeChallengePreviewForm(proposed)
    if request.method == 'POST':
        if request.POST.get('submit') == 'accept':
            challenge_req.status = ChallengeRequest.ACCEPTED
            email_msg = _("Runner %(username)s has accepted your challenge") %\
                dict(username=challenge_req.runner.username)
            msg = _("You have accepted a challenge.")
            Challenge.objects.create_for_challenge(challenge_req)
        else:  # request.POST.get('submit') == 'reject':
            challenge_req.status = ChallengeRequest.REJECTED
            email_msg = _("Runner %(username)s has rejected your challenge") %\
                dict(username=challenge_req.runner.username)
            msg = _("You have rejected a challenge.")
        challenge_req.save()
        messages.info(request, msg)
        send_mail(email_msg, email_msg, settings.DEFAULT_FROM_EMAIL,
                  [challenge_req.sponsor.email, ])
        return redirect('profile:my_page')

    context = {
        'challenge_req': challenge_req,
        'form': form
    }
    return render(request, 'challenges/preview_challenge.html', context)


@login_required
def preview_invitation_challenge(request, token=None):
    """
    Sponsor can edit challenge, accept or reject challenge invitation.
    """
    challenge_req = ChallengeRequest.objects.get(token=token)
    if challenge_req.sponsor != request.user:
        messages.info(request, _('You have been logged out, because you '
                                 'visited an invitation to a challenge '
                                 'that was sent to another user.'))
        logout(request)
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if challenge_req.status != ChallengeRequest.NEW:
        return HttpResponseForbidden('You cannot preview an invitation that '
                                     'has already been accepted or rejected.')

    form = ChallengeForm(json.loads(challenge_req.proposed_challenge))
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            if request.POST.get('submit') == 'create':
                challenge_req.status = ChallengeRequest.ACCEPTED
                ctx = Context({
                    'sponsor': challenge_req.sponsor.username,
                    'challenge_text': form.cleaned_data['challenge_text'],
                    'amount': form.cleaned_data['amount'],
                    'BASE_URL': settings.BASE_URL
                })
                tmpl = 'challenges/emails/invitation_accepted.html'
                email_subject = _('%(sponsor)s has challenged you!') % {
                    'sponsor': challenge_req.sponsor.username
                }
                email_msg = loader.get_template(tmpl).render(ctx)
                msg = _("You have created a challenge for %(username)s.") % {
                    'username': challenge_req.runner.username
                }

                Challenge.objects.create_for_challenge(challenge_req,
                                                       **form.cleaned_data)
            else:  # request.POST.get('submit') == 'reject':
                challenge_req.status = ChallengeRequest.REJECTED
                ctx = Context({
                    'sponsor': challenge_req.sponsor.username,
                    'BASE_URL': settings.BASE_URL
                })
                tmpl = 'challenges/emails/invitation_rejected.html'
                email_subject = _('%(sponsor)s rejected to challenge you.') % {
                    'sponsor': challenge_req.sponsor.username
                }
                email_msg = loader.get_template(tmpl).render(ctx)
                msg = _("You have rejected to challenge %(runner)s.") % {
                    'runner': challenge_req.runner.username
                }
            challenge_req.save()
            messages.info(request, msg)
            send_mail(email_subject,
                      '',
                      settings.DEFAULT_FROM_EMAIL,
                      [challenge_req.runner.email, ],
                      html_message=email_msg)
            return redirect('profile:my_page')

    context = {
        'challenge_request': challenge_req,
        'form': form
    }

    return render(request,
                  'challenges/preview_invitation_challenge.html',
                  context)
