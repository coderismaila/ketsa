from django.shortcuts import render


def home(request):
    return render(request, "core/base.html")


def dashboard(request):
    print(request.user.username)
    return render(request, "core/dashboard.html")
