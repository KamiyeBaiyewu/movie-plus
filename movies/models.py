from dataclasses import fields
from imp import release_lock
from turtle import up, update
from django.db import models
from django.urls import URLPattern
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Movie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    movie_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)
    ticket_price = models.PositiveIntegerField(default=1)
    rating = models.IntegerField(default=1,
                                 validators=[MaxValueValidator(5), MinValueValidator(1)])
    country = CountryField(blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='blog_images')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update', '-created']

    def __str__(self):
        return self.movie_name


class Creator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ['-created']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50] 

    class Meta:
        ordering = ['-update', '-created']
