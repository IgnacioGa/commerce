from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe

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
    idlis = Listing.objects.filter(title=title)
    listi = Listing.objects.get(title=title)
    lista = Characteristic.objects.filter(listing__in= idlis).all()
    if request.user.is_authenticated:
        us = request.user
        user = User.objects.get(id=us.id)
        WLitems = Watchlist.objects.filter(personal=user, item__title=title).values("item")
        if user == listi.creator:
            creator = str(True)
        else:
            creator = None
    else:
        WLitems = None
        creator = None
    form = Bids()

    ganador = Bid.objects.filter(listing=listi.id).order_by('bid').last() 

    comments = Comments.objects.filter(item=listi.id)
    if request.method == "POST":
        comm = request.POST["comment"]
        if comm == '':
            messages.error(request, mark_safe("Can´t be empty"))
            return HttpResponseRedirect(reverse('lis:page', args=(title,)))
        else:
            date = datetime.datetime.now()
            new = Comments(user=user, item=listi, comment=comm, date=date)
            new.save()
            return render(request, "auctions/page.html", {
                "info": idlis,
                "carac": lista,
                "form": form,
                "WL": WLitems,
                "creator": creator,
                "ganador":ganador.user, 
                "comments": comments          
            })

    return render(request, "auctions/page.html", {
            "info": idlis,
            "carac": lista,
            "form": form,
            "WL": WLitems,
            "creator": creator,
            "ganador":ganador.user, 
            "comments": comments          
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

def changeWL(request, watch):
    if request.method == 'POST':
        us = request.user
        user = User.objects.get(id=us.id)
        liss = Listing.objects.get(title=watch)
        WLitems = Watchlist.objects.filter(personal=user, item__title=watch).values("item")
        idWL = Watchlist.objects.get(personal=user)
        if WLitems:
            idWL.item.remove(liss)
        else:        
            idWL.item.add(liss)
        return HttpResponseRedirect(reverse('lis:page', args=(watch,)))

def bids(request, title):
    if request.method == 'POST':
        form = Bids(request.POST)
        us = request.user
        user = User.objects.get(id=us.id)
        if form.is_valid():
            bid = form.cleaned_data["updrageBid"]
            listing = Listing.objects.get(title=title)
            date = datetime.datetime.now()
            if listing.actualBid:
                if bid <= listing.actualBid:
                    messages.error(request, mark_safe("The bid has to be more than "+str(listing.actualBid)+""))
                    return HttpResponseRedirect(reverse('lis:page', args=(title,)))
                else:
                    Listing.objects.filter(title=title).update(actualBid=bid)
                    update = Bid(listing=listing, user=user, bid=bid, date=date)
                    update.save()
                    messages.success(request, mark_safe("Congrats, you do the bid"))
                    return HttpResponseRedirect(reverse('lis:page', args=(title,)))
            else:
                if bid < listing.initialBid:
                    messages.error(request, mark_safe("The bid has to be more than "+str(listing.initialBid)+""))
                    return HttpResponseRedirect(reverse('lis:page', args=(title,)))
                else:
                    Listing.objects.filter(title=title).update(actualBid=bid)
                    update = Bid(listing=listing, user=user, bid=bid, date=date)
                    update.save()
                    messages.success(request, mark_safe("Congrats, the bid has been done"))
                    return HttpResponseRedirect(reverse('lis:page', args=(title,)))

def status(request, title):
    if request.method == 'POST':
        listing = Listing.objects.get(title=title)
        if listing.active == True:
            listing.active = False
            listing.save()
        return HttpResponseRedirect(reverse('lis:page', args=(title,)))

def watchlist(request):
    items = []
    us = request.user
    user = User.objects.get(id=us.id)
    watch = Watchlist.objects.get(personal=user)
    WL = watch.item.all()
    for x in WL : 
        items.append(x)
    return render(request, "auctions/watchlist.html",{
            "list": items
        })

def closed(request):
    ganadas = []
    items = Listing.objects.filter(active=False)
    for x in items:
        ganador = Bid.objects.filter(listing=x.id).order_by('bid').last()
        dicc = {
            "listing": x,
            "ganador": ganador
        }
        ganadas.append(dicc) 
    return render(request, "auctions/closed.html",{
            "list": ganadas
        })
