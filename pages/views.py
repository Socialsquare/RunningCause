from django.shortcuts import render
from django.db.models import Sum

import datetime

from sponsorship.models import Sponsorship
from challenges.models import Challenge
from runs.models import Run


def contact(request):
    return render(request, 'pages/contact.html')


def generate_raised(start_date, end_date):
    sponsorships = Sponsorship.objects.all()
    challenges = Challenge.objects.all()

    challenge_filters = {}
    if start_date:
        challenge_filters['end_date__gte'] = start_date
    if end_date:
        challenge_filters['end_date__lte'] = end_date

    challenges = Challenge.objects.filter(**challenge_filters)

    sponsorships_raised = sum([float(s.total_amount_in_interval(start_date, end_date)) for s in sponsorships])
    sponsorships_paid = sum([float(s.amount_paid) for s in sponsorships])
    challenges_raised = sum([float(s.amount) for s in challenges])
    challenges_paid = sum([float(s.amount) for s in challenges.filter(status='paid')])

    raised = sponsorships_raised + challenges_raised

    outstanding = sponsorships_raised + challenges_raised
    outstanding -= sponsorships_paid + challenges_paid

    return {
        'raised': raised,
        'outstanding': outstanding
    }


def frontpage(request):
    today = datetime.date.today()

    RAISED_OFFSET = 22938.2
    total = generate_raised(None, today)
    total['raised'] += RAISED_OFFSET
    previous_12_months = generate_raised(today-datetime.timedelta(days=365), today)
    previous_3_months = generate_raised(today-datetime.timedelta(days=3*30), today)

    total_distance = Run.objects.aggregate(total_distance=Sum('distance'))['total_distance'] or 0
    dk_to_masanga = total_distance / 7411

    context = {
        'total': total,
        'previous_12_months': previous_12_months,
        'previous_3_months': previous_3_months,
        'total_distance': int(total_distance),
        'dk_to_masanga': dk_to_masanga
    }
    return render(request, 'pages/frontpage.html', context=context)
