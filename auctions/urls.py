from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("item/<int:item_id>", views.item, name="item"),
    path("createlisting", views.createListing, name="create"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("myitems", views.myitems, name="myitems"),
    path("delete/<int:item_id>", views.delete, name="delete"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add/<int:item_id>", views.addtowatchlist, name="addtowatchlist"),
    path("remove/<int:item_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("category/<str:name>", views.category, name="category"),
    path("close/<int:item_id>", views.close, name="close")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
