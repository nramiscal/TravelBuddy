# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from ..user_app.models import User, UserManager

now = str(datetime.now())

class TripManager(models.Manager):
    def tripValidator(self, form, user_id):
        place = form['place']
        desc = form['desc']
        startDate = form['startDate']
        endDate = form['endDate']

        errors = []

        if len(place) < 1:
            errors.append("Please enter a destination.")
        if len(desc) < 1:
            errors.append("Please enter a description.")
        if not startDate:
            errors.append("Please choose a departure date.")
        elif startDate < now:
            errors.append("Departure date cannot be in the past.")
        if not endDate:
            errors.append("Please choose a return date.")
        elif endDate < startDate:
            errors.append("Return date cannot be before departure date.")

        if len(errors) > 0:
            return (False, errors)
        else:
            trip = Trip.objects.create(place = place, desc = desc, startDate = startDate, endDate = endDate, planner_id=user_id)
            Join.objects.create(user_id=user_id, trip_id=trip.id)
            return (True, trip)


class Trip(models.Model):
    place = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    planner = models.ForeignKey(User, related_name = "trips")
    objects = TripManager()

    def __repr__(self):
        return "<Trip {} {}>".format(self.id, self.place)

class Join(models.Model):
    user = models.ForeignKey(User, related_name = "users")
    trip = models.ForeignKey(Trip, related_name = "trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __repr__(self):
        return "<Join: User_id = {} Trip_id = {}>".format(self.user_id, self.trip_id)
