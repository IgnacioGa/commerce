from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
	category = models.CharField(max_length=64)

	def __str__(self):
		return f"{self.id} : {self.category}"

class Listing(models.Model):
	title = models.CharField(max_length=64)
	description = models.TextField()
	initialBid = models.DecimalField(max_digits=8, decimal_places=2)
	urlImage = models.CharField(max_length=255, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="fields", blank=True, null=True)
	date = models.DateTimeField()
	actualBid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
	active = models.BooleanField()
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myListing")

	def __str__(self):
		return f"{self.id}: {self.title} for {self.creator}"

class Bid(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="prices")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
	bid = models.DecimalField(max_digits=8, decimal_places=2)
	date = models.DateTimeField()

	def __str__(self):
		return f"{self.user}: {self.listing} for {self.bid}"

class Watchlist(models.Model):
	item = models.ManyToManyField(Listing, related_name="watched")
	personal = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list")
	date = models.DateTimeField()

	def __str__(self):
		return f"{self.personal} track {self.item} sinse {self.date}"

class Comments(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coment")
	item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comented")
	comment = models.TextField()
	date = models.DateTimeField()

	def __str__(self):
		return f"{self.user} comment in {self.item}"

class Characteristic(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="details")
	characteristic = models.TextField()

	def __str__(self):
		return f"Differents {self.characteristic} for {self.listing}"



