from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_window, name="login_window"),

]