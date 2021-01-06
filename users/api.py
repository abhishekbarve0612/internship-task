from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Favourites
from .serializers import UserSerializer, FavouriteSerializer
from django.core import serializers


@api_view(["POST", "GET"])
def loginApi(request):
    data = request.data
    username = data['username']
    password = data['password']
    if request.method == "POST":
        users = User.objects.values('username', 'password')
        for u in users:
            if u['username'] == username and u['password'] == password:
                user = User.objects.get(username=username, password=password)
                auth.login(request, user)
                data["Success"] = "User has successfully logged In"
                request.session['username'] = data["username"]
                return Response(data)
        data["error"] = "Invalid Credentials, Please try again"
    return Response(data)


@api_view(["POST", ])
def SignUpAPI(request):
    data = request.data
    username = data['username']
    password = data['password']
    confpassword = data['confpassword']
    email = data['email']
    favourites = data['favourites']
    if request.method == "POST":
        if password != confpassword:
            data["error"] = "Passwords do not match"
            return Response(data)
        data['usern'] = username
        data['favourites'] = favourites
        fav_serializer = FavouriteSerializer(data=data)
        if fav_serializer.is_valid():
            fav_serializer.save()
            fs = Favourites.objects.filter(usern=username)[0]
            data['favourites'] = fs.pk
            user_serializer = UserSerializer(data=data)
            if user_serializer.is_valid():
                try:
                    email = User.objects.get(user__email=email)
                    data["error"] = "Email Already Taken"
                    return Response(data)
                except:
                    email = data['email']
                try:
                    username = User.objects.get(user__username=username)
                    data["error"] = "Username Already Taken"
                    return Response(data)
                except:
                    username = data['username']
                user_serializer.save()
                data["favourites"] = favourites.split(',')
                data["success"] = "Signed Up Successfully"
                return Response(data)
            else:
                data["error"] = user_serializer.errors
                return Response(data)
    else:
        data["error"] = "Method is not POST"
    return Response(data)


@api_view(["POST", ])
def FavouritesAPI(request):
    data = request.data
    if request.method == "POST":
        newfavourites = data['favourites']
        try:
            username = data['username']
            if username == "":
                data['error'] = "User is not logged in"
                return Response(data)
        except:
            data['error'] = "User is not logged in"
            return Response(data)
        user = User.objects.get(username=username)
        pk = user.favourites
        fav = Favourites.objects.get(pk=pk.pk)
        initialfav = fav.favourites
        if initialfav != "":
            newfav = initialfav + "," + newfavourites
        else:
            newfav = newfavourites
        data['favourites'] = newfav
        data['usern'] = user.username
        fav_serializer = FavouriteSerializer(fav, data=data)
        if fav_serializer.is_valid():
            fav_serializer.save()
            data['favourites'] = newfav.split(',')
            data["success"] = "Favourites Updated Successfully"
            return Response(data)
        else:
            data["error"] = fav_serializer.errors
            return Response(data)
    else:
        data["error"] = "Method is not POST"
    return Response(data)


@api_view(["POST", ])
def RemoveFavouritesAPI(request):
    data = request.data
    if request.method == "POST":
        try:
            username = data['username']
            if username == "":
                data['error'] = "User is not logged in"
                return Response(data)
        except:
            data['error'] = "User is not logged in"
            return Response(data)
        user = User.objects.get(username=username)
        pk = user.favourites
        fav = Favourites.objects.get(pk=pk.pk)
        initialfav = fav.favourites
        newfav = ""
        data['favourites'] = newfav
        data['usern'] = user.username
        fav_serializer = FavouriteSerializer(fav, data=data)
        if fav_serializer.is_valid():
            fav_serializer.save()
            data["success"] = "Favourites Updated Successfully"
            return Response(data)
        else:
            data["error"] = fav_serializer.errors
            return Response(data)
    else:
        data["error"] = "Method is not POST"
    return Response(data)


@api_view(["GET"])
def UserDetailsAPI(request):
    data = request.data
    username = data['username']
    user = User.objects.get(username=username)
    fav = user.favourites
    fav = fav.favourites
    fav = fav.split(',')

    data = {
        "username": user.username,
        "email": user.email,
        "favourites": fav
    }
    return Response(data)
