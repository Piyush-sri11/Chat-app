from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("home/", home, name="home"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("<str:username>/", chatPage, name="chat"),
    path("logout/", logout_user, name="logout"),
]



