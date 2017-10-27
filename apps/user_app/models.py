# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt


class UserManager(models.Manager):
    def regValidator(self, form):
        name = form['name']
        username = form['username']
        password = form['password']
        confirm_pw = form['confirm_pw']

        errors = []

        if len(name) < 3:
            errors.append("Name must be at least 3 characters.")

        if len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        elif User.objects.filter(username=username):
            errors.append("Username is already taken.")

        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm_pw:
            errors.append("Password and Password confirmation do  not match.")

        if len(errors) > 0:
            return (False, errors)
        else:
            pwhash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name = name, username = username, password = pwhash)
            return (True, user)

    def loginValidator(self, form):

        username = form['username']
        password = form['password']

        errors = []

        if len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        elif not User.objects.filter(username=username):
            errors.append("Not a registered username.")

        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        if User.objects.filter(username=username):
            user = User.objects.get(username=username)
            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                errors.append("Incorrect password: does not match password stored in database.")

        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.get(username=username)
            return (True, user)



class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return "<User {} {} {}>".format(self.id, self.name, self.username)
