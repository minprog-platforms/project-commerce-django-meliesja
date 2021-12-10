from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    """Displays page with all active listings."""
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


@login_required
def create(request):
    """Create a new listing."""
    if request.method == "POST":
        # retrieve data
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = request.POST.get("starting_bid")
        image_link = request.POST.get("image_link")
        user = request.user

        # create listing object
        listing = Listing(title=title, description=description, starting_bid=starting_bid, image_link=image_link, user=user)

        listing.save()

        # redirect user to index page
        return HttpResponseRedirect(reverse("index"))

    # redirect user to page to create new listing
    return render(request, "auctions/create.html")
 

@login_required
def listing_view(request, listing_id):
    """Display page for a single listing."""
    user = request.user
    # retrieve listing by its id
    listing = Listing.objects.get(id=listing_id)
    
    # retrieve comments of listing
    comments = listing.comments.all()

    # request method is GET 
    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "comments": comments
        })

@login_required
def comment(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(id=listing_id)
        comments = listing.comments.all() 

        comment = request.POST.get("comment")

        user = request.user

        new_comment = Comment(comment=comment, user=user, listing_id=listing)
        new_comment.save()
        
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
        })


@login_required
def bid(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(id=listing_id)
        user = request.user

        # get user submitted bid
        new_bid = float(request.POST.get("new_bid"))
    
        current_bid = float(listing.starting_bid)

        # check if user bid valid
        if new_bid <= current_bid:
            
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": listing.comments.all(),
                "warning": "Your bid must be higher than the current bid."
                })
        else:
            # update price to highest bid
            listing.starting_bid = new_bid
            listing.save()
            
            # create new bid
            new_bid_obj = Bid(bidder=user, bid=new_bid, listing_id=listing)
            new_bid_obj.save()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": listing.comments.all()
                })


@login_required
def toggle_watchlist(request, listing_id):
# def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    
    if request.method=="POST":
        # check if user has listing in watchlist
        if Watchlist.objects.filter(user=user, listing_id=listing):
            # delete listing from watchlist if it exists
            watchlist = Watchlist.objects.filter(user=user, listing_id=listing)
            watchlist.delete()

            # get user watchlist
            user_watchlist = Watchlist.objects.filter(user=User.objects.get(username=request.user))

            return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": listing.comments.all(),
                    "watchlist": user_watchlist
                })
        # user does not have listing in watchlist
        else:
            # add listing to user watchlist
            watchlist = Watchlist(listing=listing, user=user)
            watchlist.save()


    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.comments.all()
    })


@login_required
def close_listing(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(id=listing_id)
        # user = request.user

        listing.closed == True
        listing.save()
        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": listing.comments.all(),
            "message": "Listing closed"
            })
