from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, Listing, Bid, Category, Watchlist, Comments, Characteristic

from .forms import Bids, CreateLis


def index(request):
    return render(request, "auctions/index.html",{
        "titles": Listing.objects.all(),
        "car": Characteristic.objects.all(),       
            })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("lis:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("lis:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def page(request, title):
    if request.method == 'POST':
        form = Bids(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('lis:page', args=(title,)))
    else:
        form = Bids()
        idlis = Listing.objects.filter(title=title)
        lista = Characteristic.objects.filter(listing__in= idlis).all()
        return render(request, "auctions/page.html", {
                    "info": idlis,
                    "carac": lista,
                    "form": form
                })

def create(request):
    if request.method == 'POST':
        form = CreateLis(request.POST)
        us = request.user
        user = User.objects.get(id=us.id)
        if form.is_valid():
            title = form.cleaned_data["Title"]
            descripcion = form.cleaned_data["Description"]
            initialBid = form.cleaned_data["InitialBid"]
            image = form.cleaned_data["URLImagen"]
            category = form.cleaned_data["Category"]
            date = datetime.datetime.now()
            act = True
            new = Listing(title=title, description=descripcion, initialBid=initialBid, urlImage=image, category=category, date=date, active=act, creator=user)
            new.save()
            return HttpResponseRedirect(reverse('lis:page', args=(title,)))
    else:
        form = CreateLis()
        return render(request, "auctions/create.html",{
            "form": form
            })

def category(request, category):
    return render(request, "auctions/category.html",{
            "listing": Listing.objects.filter(category__category=category)
            })
