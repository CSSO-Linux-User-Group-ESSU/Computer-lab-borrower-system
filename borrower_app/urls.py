from django.urls import path
from . import views

urlpatterns = [
    path('', views.logins, name="login"),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('logout/', views.log_out, name="logout"),
    path('control_panel/', views.control_panel, name="control_panel"),
    path('home/', views.home, name="home"),
    path('pending_items/', views.pending_items, name="pending_items"),
    path('return_items/', views.return_items, name="return_items"),
    path('scan_printer/', views.scan_printer, name="scan_printer"),
    path('scan/', views.scan_paper, name="scan"),
    path('borrower/delete/', views.delete_borrowers, name='delete_borrowers'),
    path('borrower/delete/<int:borrower_id>/', views.delete_borrower, name='delete_borrower'),
    path('borrower/edit/<int:borrower_id>/', views.edit_borrower, name='modify_borrower'),
    path('upload_and_process_file/', views.upload_and_process_file, name='upload_and_process_file'),
    path('success_page/',views.success_page,name='success_page'),
    path('manual_input/', views.manual_input, name='manual_input'),
]