from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing-view"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    # path("addwatchlist/<int:listing_id>", views.add_watchlist, name="add-watchlist"),
    # path("removewatchlist/<int:listing_id>", views.remove_watchlist, name="remove-watchlist"),
    path("close/<int:listing_id>", views.close_listing, name="close-listing"),
    path("togglewatchlist/<int:listing_id>", views.toggle_watchlist, name="toggle-watchlist")


]
