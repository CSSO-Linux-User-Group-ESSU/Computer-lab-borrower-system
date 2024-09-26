from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_window, name="login_window"),
    path('main_window/', views.main_window, name="main_Window"),
]