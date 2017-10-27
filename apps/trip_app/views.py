# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import Trip, TripManager, Join
from ..user_app.models import User, UserManager


def my_page(request):
    # Join.objects.all().delete()
    # Trip.objects.all().delete()

    trips = Trip.objects.all()

    joins = Join.objects.filter(user_id=request.session['id'])

    # remove wishes that are also in joins
    for join in joins:
        trips = trips.exclude(id = join.trip_id)

    return render(request, "trip_app/my_page.html", {"trips":trips,"joins":joins})


def show(request, trip_id):
    trip = Trip.objects.get(id=trip_id)

    joins = Join.objects.filter(trip_id = trip_id)
    print joins

    data = {
        "trip" : trip,
        "joins" : joins,
    }

    return render(request, "trip_app/show.html", data)

def join(request, trip_id, user_id):
    Join.objects.create(trip_id=trip_id, user_id=user_id)
    return redirect("/my_page")


def add(request):
    return render(request, "trip_app/add.html")

def createTrip(request):
    print request.session['id']

    valid = Trip.objects.tripValidator(request.POST, request.session['id'])
    # valid = (True, trip) or (False, errors)

    if valid[0]:
        return redirect("/my_page")
    else:
        for error in valid[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/add")

    return redirect("/add")
