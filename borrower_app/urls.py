from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.logins, name="login"),
    path('sign_up/',views.signup, name='sign_up'),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('logout/', views.log_out, name="logout"),
    path('control_panel/', views.control_panel, name="control_panel"),
    path('home/', views.home, name="home"),
    path('pending_items/', views.pending_items, name="pending_items"),
    path('return_items/', views.return_items, name="return_items"),
    path('scan_printer/', views.scan_printer, name="scan_printer"),
    path('scan/', views.scan_paper, name="scan"),
    path('borrower/delete/', views.delete_borrowers, name='delete_borrowers'),
    path('return/delete/', views.delete_returns, name='delete_returns'),
    path('borrower/edit/<int:borrower_id>/', views.edit_borrower, name='edit_borrower'),
    path('upload/', views.upload_and_process_file, name='upload_and_process_file'),
    path('success_page/',views.success_page,name='success_page'),
    path('borrower_form_view/', views.borrower_form_view, name='borrower_form_view'),
    path('api/get-borrower-data/', views.get_borrower_data, name='get_borrower_data'),
    path('transfer_borrowers/', views.transfer_borrowers, name='transfer_borrowers'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)