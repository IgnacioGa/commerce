from django.urls import path

from . import views

app_name = "lis"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("page/<str:title>", views.page, name="page"),
]
