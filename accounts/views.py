from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password
from Web_Scheduler.custom import login_required_custom
from .models import Userbase

# Clear session, enter the entrance view
def entrance_view(request):
    context = {}
    request.session["user_id"] = None
    return render(request, "entrance.html", context)

# Register an account
# Do the validation
def register_view(request):
    context = {}

    # IMPORTANT
    # "POST" means user has submitted a form, otherwise "GET"
    # Meaning when this page is rendered from Entrance, it won't trigger process below
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        birthday = request.POST.get("birthday")
        checkbox = request.POST.get("checkbox1")

        if not username:
            context["hint"] = "Must Enter Username."
            context["redframe"] = "username"
            return render(request, "register.html", context)
        
        # Remember the username so that it won't have to be typed again
        context["username"] = username
        try:
            # If the query succeeded, it means the username is already taken.
            # If not, it will raise an exception.
            Userbase.objects.get(username=username)
            context["hint"] = "Username Already Taken."
            context["redframe"] = "username"
        except:
            if not password:
                context["hint"] = "Must Enter Password."
                context["redframe"] = "password"
            elif not confirmation:
                context["hint"] = "Please re-enter password."
            elif not birthday:
                context["hint"] = "Please Enter Birthday."
            elif not checkbox:
                context["hint"] = "Please read the terms & conditions."
            else:
                # Register the account into database
                Userbase.objects.create(username=username, password=make_password(password), birthday=birthday) 
                context["hint"] = "Account Created. Please Login Here."
                return redirect('/accounts/login/')

    return render(request, "register.html", context)

def login_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            context["hint"] = "Must Enter Both Fields."
            return render(request, "login.html", context=context)
        
        # Get the corresponding username an
        try:
            obj = Userbase.objects.get(username=username)
            id = obj.id
        except:
            id = None
        if id and check_password(password, make_password(password)):
            request.session["user_id"] = id
            # Use redirect when current data is no longer needed
            # It will change to a new URL also
            # Unlike render(), the URL will stay the same
            return redirect('/') 
        else:
            context["hint"] = "Invalid username or password."

    return render(request, "login.html", context=context)

@login_required_custom
def logout_view(request):
    context = {}
    return render(request, "logout.html", context)
