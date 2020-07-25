from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .checks import *
from .forms import *

# Landing page. Shows active listings regardless of loggedin/loggedout
def index(request):
    return render(request, "auctions/index.html", {
        "items": Listing.objects.all(),
        "title": 'Active Listings'
    })


# Login page. Redirects to previous page using 'next' parameter
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(redirect_to=request.GET['next'] or reverse("auctions:index"))
            else:
                return render(request, "auctions/login.html", {
                    "message": "Invalid username and/or password.",
                    "form": form
                })
    else:
        form = LoginForm()
        return render(request, "auctions/login.html", {
            "form": form
        })


# Log out page. Redirects to landing page after log out.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


# Registration page for creating new users, also creates a field in Watchlist for them.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
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
                    "message": "Username already taken.",
                    "form": form
                })
            login(request, user)
            watch = Watchlist(user=user)
            watch.save()
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        form = RegisterForm()
        return render(request, "auctions/register.html", {
            "form": form
        })


# Shows individual item and various details like bids, comments included
@login_required
def item(request, item_id):
    item = Listing.objects.get(pk=item_id)
    check = checkauthor(item_id, request.user.id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_check = checkbid(item_id, request.POST['bid'])
            if bid_check == True:
                bid = Bid(bidder=User.objects.get(pk=request.user.id), item=item, bid=request.POST['bid'])
                bid.save()
                return redirect(reverse('auctions:item', args=(item_id,)))
            else:
                return render(request, "auctions/item.html", {
                    "item": item,
                    "bids": item.bids.all().order_by('-bid'),
                    "comments": item.related.all(),
                    "message": "Your bid must be greater than current and minimum bid.",
                    "check": check,
                    "form": form,
                    "there": checkwatchlist(request.user.id, item.id)
                })
    else:
        form = BidForm()
        return render(request, "auctions/item.html", {
            "item": item,
            "bids": item.bids.all().order_by('-bid'),
            "comments": item.related.all(),
            "check": check,
            "form": form,
            "there": checkwatchlist(request.user.id, item.id)
        })


# Page to create new listing
@login_required
def createListing(request):
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            listing = Listing(title=form.cleaned_data.get('title'), category=Category.objects.get(category=form.cleaned_data.get('category')), details=form.cleaned_data.get('details'),display=form.cleaned_data.get('display'), minbid=form.cleaned_data.get('minbid'), author=User.objects.get(pk=request.user.id))
            listing.save()
            return redirect(reverse('auctions:myitems'))
    else:
        form = CreateForm()
        return render(request, "auctions/createlisting.html", {
            "form": form
        })


# Updates new comments
@login_required
def comment(request, item_id):
    if request.method == 'POST':
        comment = Comment(commenter=User.objects.get(pk=request.user.id), item=Listing.objects.get(pk=item_id), comment=request.POST['comment'])
        comment.save()
    return redirect(reverse('auctions:item', args=(item_id,)))


# Page to show author of their listings
@login_required
def myitems(request):
    return render(request, "auctions/index.html", {
        "items": User.objects.get(pk=request.user.id).myitems.all(),
        "title": 'My Listings'
    })


# Method to delete a listing, accepts a post request if confirmed 'yes'
@login_required
def delete(request, item_id):
    if request.method == 'POST':
        Listing.objects.filter(pk=item_id).delete()
        return redirect(reverse('auctions:myitems'))
    return render(request, "auctions/delete.html", {
        "title": 'Are you sure you want to delete?',
        "item_id": item_id
    })


# Page to show listings added to watchlist
@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "title": 'Watchlist',
        "items": Watchlist.objects.get(user=User.objects.get(pk=request.user.id)).items.all()
    })

# Method to add item to watchlist
@login_required
def addtowatchlist(request, item_id):
    item = Watchlist.objects.get(user=User.objects.get(pk=request.user.id))
    item.items.add(Listing.objects.get(pk=item_id))
    return redirect(reverse('auctions:item', args=(item_id,)))


# Method to remove item from watchlist
@login_required
def removefromwatchlist(request, item_id):
    item = Watchlist.objects.get(user=User.objects.get(pk=request.user.id))
    item.items.remove(Listing.objects.get(pk=item_id))
    return redirect(reverse('auctions:item', args=(item_id,)))


# Page to show items of particular category
@login_required
def category(request, name):
    name = name.title()
    items = Category.objects.get(category=name).subitems.all()
    return render(request, "auctions/index.html", {
        "items": items,
        "title": name.title()
    })

@login_required
def close(request, item_id):
    try:
        bid = item.bids.all().order_by('-bid')[0]
        item = Listing.objects.get(pk=item_id)
        item.is_open = False
        item.save()
        return render(request, "auctions/close.html", {
            "bid": bid
        })
    except:
        return redirect(reverse("auctions:item", args=(item_id,)))
