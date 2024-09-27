from django.shortcuts import render, redirect
import django.contrib.messages as messages
from .models import BorrowerInfo


# Create your views here.
def login_window(request):
    return render(request, 'borrower_app/login_index.html')


def main_window(request):
    if request.method=="POST":
        name = request.POST["username"]
        password = request.POST["password"]
        if password != "admin":
            messages.error(request, "Wrong password redirecting to home!")
            return redirect("login_window")
        return render(request, 'borrower_app/main_index.html', {"result": name})
    return redirect("login_window")


def home(request):
    return render(request, 'borrower_app/home.html')


def pending_items(request):
    return render(request, 'borrower_app/pending_items.html', {
        'all_info': BorrowerInfo.objects.all()
    })


def return_items(request):
    return render(request, 'borrower_app/return_items.html')