from django.urls import path
from . import views

urlpatterns = [
    path('', views.logins, name="login"),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('control_panel/', views.control_panel, name="control_panel"),
    path('home/', views.new_home, name="home"),
    path('pending_items/', views.pending_items, name="pending_items"),
    path('return_items/', views.return_items, name="return_items"),
    path('scan_printer/', views.scan_printer, name="scan_printer"),
]