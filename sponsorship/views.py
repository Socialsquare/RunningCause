


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
