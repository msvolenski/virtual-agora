from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User as AuthUser
from .models import Choice, Question, Answer, User, InitialListQuestion, Message, Termo
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def term_required(function):
    def wrap(request, *args, **kwargs):
        username = AuthUser.objects.get(username=request.user)
        user = username.user
        cond = Termo.objects.get(user=user)
        if cond.condition == 'Sim':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('agora:termo'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
