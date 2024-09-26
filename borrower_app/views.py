from django.shortcuts import render, redirect
import django.contrib.messages as messages


# Create your views here.
def login_window(request):
    return render(request, 'login/index.html')


def main_window(request):
    if request.method=="POST":
        name = request.POST["username"]
        password = request.POST["password"]
        if password != "admin":
            messages.error(request, "Wrong password redirecting to home!")
            return redirect("Login")
    return render(request, 'main_window/index.html', {"result": name})