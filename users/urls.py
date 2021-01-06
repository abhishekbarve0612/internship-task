from django.urls import path
from .views import *
from .api import loginApi, SignUpAPI, FavouritesAPI, RemoveFavouritesAPI, UserDetailsAPI


urlpatterns = [
    path('login-api', loginApi, name="loginApi"),
    path('signup-api', SignUpAPI, name="signup-api"),
    path('fav-api', FavouritesAPI, name="fav-api"),
    path('remove-fav-api', RemoveFavouritesAPI, name="remove-fav-api"),
    path('user-details-api', UserDetailsAPI, name="user-details-api")
]
