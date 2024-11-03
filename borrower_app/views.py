from django.shortcuts import render, redirect, get_object_or_404
import django.contrib.messages as messages
from .models import BorrowerInfo
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
import subprocess
import json
import cv2
from .form import BorrowerForm
from datetime import date


def upload_and_process_file(request):
    if request.method == 'POST':
        form = BorrowerForm(request.POST)

        if form.is_valid():
            borrower = form.save(commit=False)
            if not borrower.date_borrowed:
                borrower.date_borrowed = date.today()
            borrower.save()
            messages.success(request, "Borrower saved successfully.")
            return redirect('success_page')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'borrower_app/home.html', {'form': form})

    # Provide an empty form if GET request
    form = BorrowerForm()
    return render(request, 'borrower_app/form.html', {'form': form})


def success_page(request):
    return render(request, "borrower_app/success_page.html")


def manual_input(request):
    return render(request, 'borrower_app/form.html')


# Create your views here.
def logins(request):
    return render(request, 'borrower_app/login.html')


def sign_in(request):
    return render(request, 'borrower_app/sign_in.html')


def log_out(request):
    logout(request)
    return redirect('/')


def control_panel(request):
    if request.method == "POST":
        name = request.POST.get("username")  # Safely retrieve the username
        password = request.POST.get("password")  # Safely retrieve the password

        # Authenticate the user
        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Wrong username or password! Please try again.")
            return redirect('login')  # Redirect to the login page on error

    return render(request, 'borrower_app/login.html')  # Render the login page for GET requests


@login_required
def home(request):
    return render(request, 'borrower_app/home.html')


def return_items(request):
    return render(request, 'borrower_app/return_items.html')


def pending_items(request):
    borrowers = BorrowerInfo.objects.all()
    return render(request, 'borrower_app/pending_items.html', {'borrowers': borrowers})


def delete_borrower(request, borrower_id):
    borrower = get_object_or_404(BorrowerInfo, id=borrower_id)

    if request.method == "POST":
        borrower.delete()
        messages.success(request, "Borrower deleted successfully!")
        return redirect('pending_items')

    return render(request, 'borrower_app/confirm_delete.html', {'borrower': borrower})


def delete_borrowers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        borrower_ids = data.get('borrower_ids', [])

        # Delete the borrowers with the provided IDs
        BorrowerInfo.objects.filter(id__in=borrower_ids).delete()

        # Return a success response
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def edit_borrower(request, borrower_id):
    borrower = get_object_or_404(BorrowerInfo, id=borrower_id)
    if request.method == 'POST':
        borrower.last_name = request.POST.get('last_name', borrower.last_name)
        borrower.first_name = request.POST.get('first_name', borrower.first_name)
        borrower.middle_name = request.POST.get('middle_name', borrower.middle_name)
        borrower.item_name = request.POST.get('item_name', borrower.item_name)
        borrower.item_quantity = request.POST.get('item_quantity', borrower.item_quantity)
        borrower.save()
        return redirect('pending_items')
    return render(request, 'borrower_app/edit_borrower.html', {'borrower': borrower})


def scan_printer(request):
    has_printer = subprocess.check_output('lpstat -p', shell=True)
    print(has_printer, 'has_printer')
    if b'disabled' in has_printer:
        return HttpResponse('No Printer')
    else:
        return HttpResponse('Has Printer')


def scan_paper(request):
    image_path = 'HTR/scannedImages/scanned_form.png'
    with open(image_path, 'wb') as f:
        is_scan = subprocess.run('scanimage --format=png --mode Color --resolution 600 --brightness 50 --contrast 50',
                                 stdout=f, shell=True)
        if is_scan.returncode == 0:

            # Cropping the scanned image
            image = cv2.imread(image_path)
            h, w, _ = image.shape
            image = image[:, :w // 2]
            cv2.imwrite(image_path, image)

            # Doing now the actual scanning
            scan = subprocess.run(f'python3 HTR/ocr.py {image_path}', shell=True)
            if scan.returncode == 0:
                return HttpResponse('Scanned')
            else:
                return HttpResponse('Not Scanned')
        else:
            return HttpResponse('Not Scanned')
