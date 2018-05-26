# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as AuthUser
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import *
from agoraunicamp.models import *


