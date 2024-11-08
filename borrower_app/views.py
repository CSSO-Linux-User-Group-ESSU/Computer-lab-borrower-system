from django.shortcuts import render, redirect, get_object_or_404
import django.contrib.messages as messages
from .models import BorrowerInfo, ReturnedInfo
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
import subprocess
import json
import cv2
from .form import BorrowerForm
from datetime import date
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

    


@csrf_exempt
def transfer_borrowers(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            borrower_ids = data.get("borrower_ids", [])
            
            if not borrower_ids:
                return JsonResponse({"success": False, "message": "No items selected for transfer."})
            
            # Log to verify receipt of IDs
            print("Received borrower IDs for transfer:", borrower_ids)

            successful_transfers = []
            errors = []

            for borrower_id in borrower_ids:
                try:
                    borrower = BorrowerInfo.objects.get(id=borrower_id)
                    
                    # Create a ReturnedItem instance
                    returned_item = ReturnedInfo.objects.create(
                        last_name=borrower.last_name,
                        first_name=borrower.first_name,
                        middle_name=borrower.middle_name,
                        item_name=borrower.item_name,
                        item_quantity=borrower.item_quantity,
                        date_borrowed=borrower.date_borrowed,
                    )
                    
                    # Confirm the transfer by checking if returned_item was created
                    if returned_item:
                        successful_transfers.append(borrower_id)
                        # Delete the Borrower record only if transfer was successful
                        borrower.delete()
                    else:
                        errors.append(f"Failed to create ReturnedItem for borrower ID {borrower_id}")

                except BorrowerInfo.DoesNotExist:
                    errors.append(f"Borrower with ID {borrower_id} does not exist.")
                except Exception as e:
                    errors.append(f"Error transferring borrower ID {borrower_id}: {str(e)}")
            
            # Provide feedback on which IDs were successfully transferred or had issues
            if successful_transfers:
                success_message = f"Items successfully transferred and deleted: {successful_transfers}"
            else:
                success_message = "No items were successfully transferred."

            error_message = f"Issues with the following items: {errors}" if errors else "No issues."

            return JsonResponse({
                "success": True if successful_transfers else False,
                "message": success_message,
                "errors": error_message,
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid data format."})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})






def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not password2:
            messages.error(request, "Password confirmation is required.")
            return redirect("sign_up")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("sign_up")
        user, created = User.objects.get_or_create(username=username, email=email)

        if created:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, "User created successfully.")
            return render(request, "borrower_app/home.html")

        else:
            messages.error(request, "User already exists.")
            return redirect("sign_in")

    return render(request, "borrower_app/sign_in.html")




def read_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines() 
        return [line.strip() for line in lines]
    except FileNotFoundError:
        print("Pota ka wara didi")
        return None

def borrower_form_view(request):
    data = get_borrower_data()
    forms = BorrowerForm(initial=data)
    return render(request, 'borrower_app/form.html',context={"form":forms})
        


def get_borrower_data():
    file_path = "HTR/data/data.txt"
    txt_data = read_txt_file(file_path)
    print(txt_data)

    if txt_data:
        last_name = txt_data[0].title()
        first_name = txt_data[1].title()
        middle_name = txt_data[2].title()
        item_name = txt_data[3].title()
        item_quantity =int(txt_data[4])

        borrower_data = {
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'item_name': item_name,
            'item_quantity': item_quantity,
            'date_borrowed': txt_data[5] if len(txt_data) > 5 else '',
        }
    else:
        borrower_data = {
            'last_name': '',
            'first_name': '',
            'middle_name': '',
            'item_name': '',
            'item_quantity': 0,
            'date_borrowed': '',
        }

    return borrower_data



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
    return render(request, "borrower_app/form.html")


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
    returned_items = ReturnedInfo.objects.all()
    return render(request, "borrower_app/return_items.html", {"returned_items": returned_items})



def pending_items(request):
    if request.method=="POST":
        form = BorrowerForm(request.POST)

        if form.is_valid():
            form.save()
    borrowers = BorrowerInfo.objects.all()
    return render(request, 'borrower_app/pending_items.html', {'borrowers': borrowers})



def delete_borrowers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        borrower_ids = data.get('borrower_ids', [])

        BorrowerInfo.objects.filter(id__in=borrower_ids).delete()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def delete_returns(request):
    if request.method == "POST":
        data = json.loads(request.body)
        borrower_ids = data.get('borrower_ids', [])

        ReturnedInfo.objects.filter(id__in=borrower_ids).delete()

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
        if is_scan.returncode != 0:

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
    
    return HttpResponse('No Scanner Connected.')
