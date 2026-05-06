from django.urls import path
from .views import home, register_tourist

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_tourist, name="register"),
]