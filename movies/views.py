from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.db.models import Q
from .models import Movie, Message
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.


def home(request):

    movies = Movie.objects.all()
    movie_count = movies.count()

    context = {'movies': movies, 'movie_count': movie_count}
    return render(request, 'movies/home.html', context)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"


@login_required(login_url='loginpage')
def createpage(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = MovieForm()
    return render(request, 'movies/createpage.html', {'form': form})


def loginpage(request):
    page = 'loginpage'
    if request.user.is_authenticated:
        return redirect('createpage')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist ")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 'Username or password does not exist', context)

    context = {"page": page}
    return render(request, 'movies/loginpage.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerpage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error occured during registration')

    return render(request, 'movies/login_register.html', {'form': form})


@login_required(login_url='loginpage')
def moviepage(request, pk):
    movie = Movie.objects.get(id=pk)
    movie_messages = movie.message_set.all().order_by('-created')
    # paricipants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            movie=movie,
            body=request.POST.get('body')
        )
        # room.participants.add(request.user)
        return redirect('moviepage', pk=movie.id)

    context = {'movie': movie, 'movie_messages': movie_messages}
    return render(request, 'movies/moviepage.html', context)


@login_required(login_url='loginpage')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'movies/delete.html', {'obj': message})
