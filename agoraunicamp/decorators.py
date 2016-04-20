# -*- coding: utf-8 -*-
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User as UserSys
from .models import User, Termo
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def term_required(function):
    def wrap(request, *args, **kwargs):
        try:
            us = User.objects.get(user=request.user)
        except:
            u = UserSys.objects.get(username=request.user)
            x = User(user=u, primeiro_nome="x", ultimo_nome="y", projeto="default")
            x.save()
            us = User.objects.get(user=request.user)
        cond = Termo.objects.get(user=us)
        print (cond.condition)
        if cond.condition == 'Sim':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('agoraunicamp:termo'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
