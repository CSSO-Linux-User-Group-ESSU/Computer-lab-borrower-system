from django.shortcuts import render, redirect, get_object_or_404
import django.contrib.messages as messages
from .models import BorrowerInfo
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.http import HttpResponse
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

        if password == "admin":
            return render(request, 'borrower_app/home.html')
        else:
            messages.error(request,"Wrong admin or password")
            return redirect("login_window")
    return render(request, 'borrower_app/home.html')


# def control_panel(request):
#     if request.method == "POST":
#         name = request.POST.get("username")  # Safely retrieve the username
#         password = request.POST.get("password")  # Safely retrieve the password
#
#         # Authenticate the user
#         user = authenticate(request, username=name, password=password)
#
#         if user is not None:
#             login(request, user)  # Log the user in
#             return redirect('home')  # Redirect to the home page after successful login
#         else:
#             messages.error(request, "Wrong username or password! Please try again.")
#             return redirect('login_window')  # Redirect to the login page on error
#
#     return render(request, 'borrower_app/login.html')  # Render the login page for GET requests


def home(request):
    return render(request, 'borrower_app/home.html')


def return_items(request):
    return render(request, 'borrower_app/return_items.html')


def pending_items(request):
    borrowers = BorrowerInfo.objects.all()
    borrower_data = []
    for borrower in borrowers:
        total = borrower.total_quantity()
        borrower_data.append({
            'id': borrower.id,  # Ensure borrower.id is passed here
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
    return render(request, 'borrower_app/pending_items.html', {'borrowers': borrower_data})



# Existing views...

def delete_borrower(request, borrower_id):
    borrower = get_object_or_404(BorrowerInfo, id=borrower_id)

    if request.method == "POST":
        borrower.delete()
        messages.success(request, "Borrower deleted successfully!")
        return redirect('pending_items')

    return render(request, 'borrower_app/confirm_delete.html', {'borrower': borrower})



def delete_borrowers(request):
    if request.method == "POST":
        # Get the list of borrower IDs from the request
        import json
        data = json.loads(request.body)
        borrower_ids = data.get('borrower_ids', [])

        # Delete the borrowers with the provided IDs
        BorrowerInfo.objects.filter(id__in=borrower_ids).delete()

        # Return a success response
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def pending_items(request):
    borrowers = BorrowerInfo.objects.all()
    borrower_data = []
    for borrower in borrowers:
        total = borrower.total_quantity()
        borrower_data.append({
            'id': borrower.id,  # Include the borrower ID for delete functionality
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
    return render(request, 'borrower_app/pending_items.html', {'borrowers': borrower_data})



# Edit Borrower View
def edit_borrower(request, borrower_id):
    borrower = get_object_or_404(BorrowerInfo, id=borrower_id)

    if request.method == "POST":
        # Update borrower fields with data from the form
        borrower.last_name = request.POST.get('last_name')
        borrower.first_name = request.POST.get('first_name')
        borrower.middle_name = request.POST.get('middle_name')
        borrower.led_qty = request.POST.get('led_qty')
        borrower.monitor_qty = request.POST.get('monitor_qty')
        borrower.keyboard_qty = request.POST.get('keyboard_qty')
        borrower.mouse_qty = request.POST.get('mouse_qty')
        borrower.cpu_qty = request.POST.get('cpu_qty')
        borrower.ups_qty = request.POST.get('ups_qty')
        borrower.sub_cord_qty = request.POST.get('sub_cord_qty')
        borrower.save()
        return redirect('pending_items')  # Redirect to the pending items page after saving

    return render(request, 'borrower_app/edit_borrower.html', {'borrower': borrower})

def scan_printer(request):
    has_printer = subprocess.call(['lpstat', '-p'])
    context = {'has_printer': has_printer}
    if has_printer:
        return HttpResponse('Has Printer')
    else:
        return HttpResponse('No Printer')

