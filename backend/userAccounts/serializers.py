from dataclasses import field
from django.shortcuts import render, redirect
from django.contrib.auth.models import GroupManager
from django.contrib import messages


from rest_framework import serializers
from .models import NewUser
from djoser.conf import settings 

# Displays the User Model in JSON form
class UserSerializer(serializers.ModelSerializer):
 class Meta:
        model= NewUser
        fields = '__all__'


