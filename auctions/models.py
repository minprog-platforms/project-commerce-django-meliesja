from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    starting_bid = models.FloatField()
    image_link = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Item: {self.title}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField(blank=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid amount: {self.bid} for listing: {self.listing_id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment}"

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")

    def __str__(self):
        return f"{self.listing}"
