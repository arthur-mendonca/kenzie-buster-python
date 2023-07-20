from django.db import models
from django.contrib.auth import get_user_model
from users.models import User


class MovieChoices(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20, choices=MovieChoices.choices, default=MovieChoices.G
    )
    synopsis = models.TextField(null=True, default=None)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="movies"
    )
    orders = models.ManyToManyField(
        User, through="movies.MovieOrder", related_name="orders"
    )


class MovieOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_user")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="orders_movie"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = models.DateTimeField(auto_now_add=True)
