# -*- coding: utf-8 -*-
from datetime import timedelta
from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


