from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegisterForm


def home(request):

    if request.method == "POST":

        username = request.user.username if request.user.is_authenticated else "Guest"
        age      = request.POST.get("age", "N/A")
        gender   = request.POST.get("gender", "N/A")
        weight   = request.POST.get("weight", "N/A")
        height   = request.POST.get("height", "N/A")
        bp       = request.POST.get("bp", "N/A")
        glucose  = request.POST.get("glucose", "N/A")
        symptoms = request.POST.get("symptoms", "N/A")

        email_message = f"""
New Health Checkup Form Submitted
===================================

Username       : {username}
Age            : {age}
Gender         : {gender}
Weight         : {weight} kg
Height         : {height} cm
Blood Pressure : {bp}
Glucose Level  : {glucose}
Symptoms       : {symptoms}

===================================
This was submitted via the Smart Body Checkup website.
"""

        try:
            send_mail(
                subject="New Health Checkup Form Submission",
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["amitsenjaliya043@gmail.com"],
                fail_silently=False,
            )
            print("CHECKUP EMAIL SENT SUCCESSFULLY")
        except Exception as e:
            print("CHECKUP EMAIL ERROR:", e)

    return render(request, "index.html")


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            patient = form.save(commit=False)
            patient.user = user
            patient.save()

            login(request, user)

            return redirect("/profile/")

    else:

        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("/profile/")

    return render(request, "login.html")


def user_logout(request):

    logout(request)

    return redirect("/")


@login_required(login_url="/login/")
def profile(request):

    from prediction.models import Prediction

    prediction_count = Prediction.objects.filter(user=request.user).count()

    return render(request, "dashboard.html", {
        "prediction_count": prediction_count,
    })