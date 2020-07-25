from .models import *

def checkauthor(item_id, user_id):
    item = Listing.objects.get(pk=item_id)
    user = User.objects.get(pk=user_id)
    if item.author.username == user.username:
        return True
    else:
        return False

def checkbid(item_id, now_bid):
    item = Listing.objects.get(pk=item_id)
    try:
        max_bid = item.bids.all().order_by('-bid').first().bid
        if int(now_bid) > max_bid:
            return True
        else:
            return False 
    except:
        if int(now_bid) >= item.minbid:
            return True 
        else:
            return False

def checkwatchlist(user_id, item_id):
    try:
        item = Watchlist.objects.get(user=User.objects.get(pk=user_id), items=Listing.objects.get(pk=item_id))
        return True
    except:
        return False