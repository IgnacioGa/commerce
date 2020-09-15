from django.urls import path

from . import views

app_name = "lis"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("page/<str:title>", views.page, name="page"),
    path("create", views.create, name="create"),
    path("category/<str:category>", views.category, name="category"),
    path("changeWL/<str:watch>", views.changeWL, name="changeWL"),
    path("bids/<str:title>", views.bids, name="bids"),
    path("status/<str:title>", views.status, name="status"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closed", views.closed, name="closed"),
]
