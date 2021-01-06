from django.db import models
from django.contrib.auth.models import AbstractUser


class Favourites(models.Model):
    favourites = models.TextField(blank=True, null=True)
    usern = models.CharField(max_length=120)


class User(AbstractUser):
    favourites = models.ForeignKey(Favourites, on_delete=models.CASCADE)
