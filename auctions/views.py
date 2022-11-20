from ast import Pass
from tkinter import N
#from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bid, Category
from .forms import ListingForm, CommentForm, BidForm, CloseForm


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings":listings
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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


def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.created_by=request.user
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm()

    return render(request, "auctions/create.html", {'form': form} )


def listing(request, list):
    listing = Listing.objects.get(id=list)
    comments = listing.comment_set.all().order_by('-id')
    bid = listing.bid_set.all().order_by('-bid').first()
    won_user = None if bid is None else bid.user

    new_comment = Comment(listing=listing)

    bid_form = None
    if request.user.is_authenticated:
        new_bid = Bid(user=request.user ,listing=listing)
        bid_form = BidForm(instance=new_bid)

    comment_form = CommentForm(instance=new_comment)
    close_form = CloseForm(instance=listing, initial ={
        'temp_id': listing.id,
        'won_by' : won_user,
        'closed': True
        })

    return render(request, "auctions/listing.html", {
        "listing":listing,
        "comments":comments,
        "bid":bid,
        'bid_form':bid_form,
        'comment_form':comment_form,
        'close_form':close_form
    })


def watchlist(request):
    watchlist = request.user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "list":watchlist
    })


def add(request):
    if request.method == "POST":
        listing_id = int(request.POST["listing"])


    listing = Listing.objects.get(id=listing_id)

    request.user.watchlist.add(listing)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def delete(request):
    if request.method == "POST":
        listing_id = int(request.POST["listing"])


    listing = Listing.objects.get(id=listing_id)

    request.user.watchlist.remove(listing)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def post_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            form.user = request.user
            form.save()
        
    return HttpResponseRedirect(reverse("index"))
    

def submit_bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            f = form.save(commit=False)
            high_bid = f.listing.bid_set.all().order_by('-bid').first()
            high_bid = f.listing.startbid if high_bid is None else high_bid

            print(f.bid)
            print(high_bid.bid)

            if f.bid > high_bid.bid:
                f.save()
                return render(request, "auctions/redirect.html", {
                    "message": "TEST",
                    "list" : f.listing
                    })
        
    return render(request, "auctions/redirect.html", {
                "message": "You have to bid higher.",
                "list" : f.listing
                })


def categories(request):
    categories = Category.objects.all()
    print(categories)
    return render(request, "auctions/categories.html", {
        "cat":categories
    })


def category(request,cat):
    listings = Listing.objects.filter(cat=cat)
    return render(request, "auctions/category.html", {
        "listings":listings
    })


def close(request):
    if request.method == "POST":
        listing = Listing.objects.get(id=request.POST.get("temp_id"))
        form = CloseForm(request.POST, instance=listing)

        if form.is_valid():
            f = form.save(commit=False)
            #f.won_by = request.user
            f.closed=True
            f.save()
            print("ok")

            return render(request, "auctions/redirect.html", {
                "message": "You have closed the listing.",
                "list": listing
                })

    return render(request, "auctions/redirect.html", {
        "message": "Something went wrong",
        "list": listing
        })