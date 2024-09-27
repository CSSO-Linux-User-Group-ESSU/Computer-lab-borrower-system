from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_window, name="login_window"),
    path('main_window/', views.main_window, name="main_window"),
    path('home/', views.home, name="home"),
    path('pending_items/', views.pending_items, name="pending_items"),
    path('return_items/', views.return_items, name="return_items"),
]