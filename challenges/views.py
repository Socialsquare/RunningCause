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

from common.helpers import send_email

from .models import Challenge, ChallengeRequest
from .forms import ChallengeForm, ChallengeFeedbackForm, ChallengeChallengePreviewForm
from django.http.response import HttpResponseForbidden, HttpResponseNotFound,\
    HttpResponseRedirect


log = logging.getLogger(__name__)


@login_required
def challenge_runner(request, runner_id=None):
    """
    Sponsor creates a challenge for a runner with person_id.
    """
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge_fields = {
                'runner': form.cleaned_data['runner'],
                'sponsor': request.user,
                'amount': form.cleaned_data['amount'],
                'end_date': form.cleaned_data['end_date'],
                'challenge_text': form.cleaned_data['challenge_text']
            }

            # TODO: Turn this into a contraint on the model instead
            if challenge_fields['runner'] == challenge_fields['sponsor']:
                return HttpResponseForbidden()

            challenge = Challenge.objects.create(**challenge_fields)

            subject = _('%(username)s has challenged you') % {
                'username': challenge.sponsor.username
            }
            email_context = {
                'sponsor': challenge.sponsor.username,
                'amount': challenge.amount,
                'challenge_text': challenge.challenge_text,
                'end_date': challenge.end_date
            }
            send_email(challenge.runner.email,
                       subject,
                       'challenges/emails/challenge_runner.html',
                       email_context)
            msg = _("You have just challenge %(username)s") % {
                'username': challenge.runner.username
            }
            messages.info(request, msg)
            return redirect('profile:overview', user_id=challenge.runner.id)
    else:
        if runner_id:
            runner = get_object_or_404(get_user_model(), pk=runner_id)
        else:
            runner = None

        form = ChallengeForm(initial={
            'runner': runner
        })

    # When adding a sponsorship, the sponser is always the current user
    del form.fields['sponsor']

    context = {
        'form': form
    }
    return render(request, 'challenges/challenge_runner.html', context)


@login_required
def invite_sponsor_to_challenge(request, sponsor_id=None):
    """
    Invites a user with person_id to sponsor a challenge for the user
    currently logged in.
    """
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            runner = request.user
            sponsor = form.cleaned_data['sponsor']
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

            if runner == sponsor:
                return HttpResponseForbidden()

            email_context = {
                'runner': runner.username,
                'link': full_link,
                'challenge_text': form.cleaned_data['challenge_text']
            }
            send_email([sponsor.email],
                       _('Masanga Runners invitation to challenge'),
                       'challenges/emails/invite_sponsor_to_challenge.html',
                       email_context)

            messages.info(request, _("You have send invitation"
                                     " to %(username)s to challenge you.") %\
                          dict(username=challenge_req.sponsor.username))
            return redirect('profile:overview', user_id=sponsor.id)
    else:
        if sponsor_id:
            sponsor = get_object_or_404(get_user_model(), pk=sponsor_id)
        else:
            sponsor = None

        form = ChallengeForm(initial={
            'sponsor': sponsor
        })

        # When requesting a challenge, the runner is always the current user
        del form.fields['runner']

    context = {
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
                                            'runner_id': challenge.runner.id
                                         })

                absolute_link = request.build_absolute_uri(email_link)
                email_context = {
                    'runner': challenge.runner.username,
                    'challenge_text': challenge.challenge_text,
                    'runners_message': challenge.runner_msg,
                    'link': absolute_link
                }
                send_email([challenge.sponsor.email],
                           email_subject,
                           email_template,
                           email_context)

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
                            "quarter. Thank you for making a change in "
                            "Masanga!")
                    email_subject = _("%(sponsor)s accepted to pay!") % {
                        'sponsor': challenge.sponsor.username
                    }
                    email_template = 'challenges/emails/challenge_confirmed.html'
                else:  # request.POST.get('submit') == 'decline':
                    challenge.status = Challenge.DECLINED
                    msg = _("You have declined to pay for the challenge.")
                    email_subject = _("%(sponsor)s rejected to pay!") % {
                        'sponsor': challenge.sponsor.username
                    }
                    email_template = 'challenges/emails/challenge_rejected.html'

                email_context = {
                    'sponsor': challenge.runner.username,
                    'amount': challenge.amount,
                    'challenge_text': challenge.challenge_text,
                    'runners_message': challenge.runner_msg,
                    'sponsors_message': challenge.sponsor_msg
                }
                send_email([challenge.runner.email],
                           email_subject,
                           email_template,
                           email_context)
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
                email_context = {
                    'sponsor': challenge_req.sponsor.username,
                    'challenge_text': form.cleaned_data['challenge_text'],
                    'amount': form.cleaned_data['amount']
                }
                email_template = 'challenges/emails/invitation_accepted.html'
                email_subject = _('%(sponsor)s has challenged you!') % {
                    'sponsor': challenge_req.sponsor.username
                }
                msg = _("You have created a challenge for %(username)s.") % {
                    'username': challenge_req.runner.username
                }

                Challenge.objects.create_for_challenge(challenge_req,
                                                       **form.cleaned_data)
            else:  # request.POST.get('submit') == 'reject':
                challenge_req.status = ChallengeRequest.REJECTED
                email_context = {
                    'sponsor': challenge_req.sponsor.username
                }
                email_template = 'challenges/emails/invitation_rejected.html'
                email_subject = _('%(sponsor)s rejected to challenge you.') % {
                    'sponsor': challenge_req.sponsor.username
                }
                msg = _("You have rejected to challenge %(runner)s.") % {
                    'runner': challenge_req.runner.username
                }
            challenge_req.save()
            messages.info(request, msg)
            send_email([challenge_req.runner.email],
                       email_subject,
                       email_template,
                       email_context)
            return redirect('profile:my_page')

    context = {
        'challenge_request': challenge_req,
        'form': form
    }

    return render(request,
                  'challenges/preview_invitation_challenge.html',
                  context)
