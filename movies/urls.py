from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('createpage/', views.createpage, name="createpage"),
    path('loginpage/', views.loginpage, name="loginpage"),
    path('logout/', views.logoutUser, name="logout"),
    path('registerpage/', views.registerpage, name="registerpage"),
    path('moviepage/<str:pk>/', views.moviepage, name="moviepage"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),


]
