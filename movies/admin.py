from django.contrib import admin

# Register your models here.
from .models import Movie, Creator, Message

admin.site.register(Movie)
admin.site.register(Creator)
admin.site.register(Message)
