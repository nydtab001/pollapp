from json import dumps
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from pollhome.forms import UserRegisterForm, Buttonform
from pollhome.models import Vote
from django.contrib.auth import logout


def has_voted(user):
    return user.vote.has_voted == True


def has_not_voted(user):
    return user.vote.has_voted == False


@login_required
@transaction.atomic
@user_passes_test(has_not_voted, login_url=reverse_lazy('start'))
def home(request):
    # Handle POST requests (when a button is clicked)
    if request.method == 'POST':
        # Create a Buttonform instance from the POST data
        form = Buttonform(request.POST)
        if form.is_valid():
            # Get the value of the "sub" field from the form data
            sub = form.cleaned_data['sub']

            # Get the Vote object for the current user
            clicked_button = get_object_or_404(Vote, user=request.user)

            clicked_button.has_voted = True
            # Update the Vote object based on the value of "sub"
            if sub == 'red':
                clicked_button.choice = True
                clicked_button.save()
                return redirect('results')
            elif sub == 'blue':
                clicked_button.choice = False
                clicked_button.save()
                return redirect('results')
    else:
        # If not a POST request, create blank Buttonform instance
        form = Buttonform()

    # Render the home template with the form instance
    return render(request, 'pollhome/home.html', {'form': form})


def register(request):
    # Handle POST requests (when a user submits the registration form)
    if request.method == 'POST':
        # Create a UserRegisterForm instance from the POST data
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the new User object
            form.save()

            # Display a success message using django.contrib.messages
            messages.success(request, f'Your account has been created!')

            # Get the new user's username and password from the form data
            username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            # Log the user in if they were successfully authenticated
            if user is not None:
                login(request, user)
                return redirect('poll-home')
            messages.error(request, f'not authentic!')
    else:
        form = UserRegisterForm()
    return render(request, 'pollhome/register.html', {'form': form})


@login_required
@user_passes_test(has_voted, login_url=reverse_lazy('poll-home'))
def results(request):
    count = Vote.objects.filter(choice=True).count()
    total = Vote.objects.filter(has_voted=True).count()
    percentage = count / total * 100
    return render(request, 'pollhome/results.html', {'result': round(percentage), 'total': total})


def logout_view(request):
    logout(request)
    # Redirect to start page.
    return redirect('start')


def start(request):
    return render(request, 'pollhome/start.html')
