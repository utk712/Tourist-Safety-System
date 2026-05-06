from django.shortcuts import render, redirect
from .models import Tourist


def home(request):
    return render(request, "home.html")


def register_tourist(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        country = request.POST.get("country")

        Tourist.objects.create(
            name=name,
            email=email,
            phone=phone,
            country=country
        )

        return redirect("/")

    return render(request, "register.html")