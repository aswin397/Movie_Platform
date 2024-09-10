from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Category model for movies
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique category names

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"  # Plural form in admin
        ordering = ['name']  # Sort categories alphabetically

# Movie model
class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1)
    overview = models.TextField()
    poster = models.ImageField(upload_to='posters/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey to Category

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']  # Sort movies by latest release date

# Review model
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    class Meta:
        unique_together = ('movie', 'user')  # Ensure each user can only review a movie once

    def __str__(self):
        return f'Review by {self.user} for {self.movie}'

    def clean(self):
        """Ensure the rating is between 1 and 10."""
        if not (1 <= self.rating <= 10):
            raise ValidationError("Rating must be between 1 and 10.")
