from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    details = models.CharField(max_length=1500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myitems")
    display = models.ImageField(upload_to="images/")
    minbid = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subitems")
    created_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}:{ self.title }"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="related")
    comment = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField(blank = True)
    created_on = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Listing)
