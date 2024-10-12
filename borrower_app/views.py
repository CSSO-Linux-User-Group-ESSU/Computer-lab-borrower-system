from django.shortcuts import render, redirect
import django.contrib.messages as messages
from .models import BorrowerInfo
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User
import subprocess


# Create your views here.
def logins(request):
    return render(request, 'borrower_app/login.html')

def sign_in(request):
    return render(request, 'borrower_app/sign_in.html')

def control_panel(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = authenticate(request, username=username, password=password)
            login(request,user)
            return redirect("home")
        except User.DoesNotExist:
            return redirect("login")
        
    return redirect("login")

# def new_ui(request):
#     if request.method=="POST":
#         name = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=name,password=password)
#         if user is not None:
#             login(request, user)
#             return render(request, 'borrower_app/control_panel.html')
#         else:
#             messages.error(request, "Wrong password redirecting to home!")
#             return redirect("login_window")
#     return render(request, 'borrower_app/control_panel.html')


def new_home(request):
    return render(request, 'borrower_app/home.html')


def return_items(request):
    return render(request, 'borrower_app/return_items.html')


def pending_items(request):
    borrowers = BorrowerInfo.objects.all()
    borrower_data = []
    for borrower in borrowers:
        total = borrower.total_quantity()
        borrower_data.append({
            'last_name': borrower.last_name,
            'first_name': borrower.first_name,
            'middle_name': borrower.middle_name,
            'led_qty': borrower.led_qty,
            'monitor_qty': borrower.monitor_qty,
            'keyboard_qty': borrower.keyboard_qty,
            'mouse_qty': borrower.mouse_qty,
            'cpu_qty': borrower.cpu_qty,
            'ups_qty': borrower.ups_qty,
            'sub_cord_qty': borrower.sub_cord_qty,
            'total': total,
        })
    return render(request, 'borrower_app/pending_items.html', {'borrowers': borrower_data}, )

def scan_printer(request):
    has_printer = subprocess.call(['lpstat', '-p'])
    context = {'has_printer': has_printer}
    if has_printer:
        return HttpResponse('Has Printer')
    else:
        return HttpResponse('No Printer')
    
def scan_paper(request):
    image_path = '/HTR/scannedImages/scanned_form.png'
    with open(image_path, 'wb') as f:
        subprocess.run(['scanimage', '--format=png', '--mode', 'Color', '--resolution', '300' ], stdout=f)
    scanned = subprocess.call(['python3', 'HTR/ocr.py', image_path])
    if scanned:
        return HttpResponse('Scan Complete')
    else:
        return HttpResponse('Scan Incomplete')
