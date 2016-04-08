# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from agora.models import Choice, Question, User, InitialListQuestion, Message, MeuEspacoArtigo
from .decorators import term_required
from django.views import generic




@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class AgoraConfiguracaoView(generic.ListView):
  template_name = 'agoraunicamp/agora-configuracoes.html'

  def get_context_data(self, **kwargs):
    context = super(AgoraConfiguracaoView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    return context

  def get_queryset(self):
    return


@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class AgoraView(generic.ListView):
  template_name = 'agoraunicamp/agora-inicial.html'

  def get_queryset(self):
    return

  def get_context_data(self, **kwargs):
    context = super(AgoraView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    return context

def agoraconfiguracaoapelido(request):
    username = AuthUser.objects.get(username=request.user)
    user = username.user
    apelido = request.POST['text-apelido']
    if apelido:
        apelido_user = User.objects.get(user=user)
        apelido_user.nickname = apelido
        apelido_user.save()
        success = True
    else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
        return redirect(request.META['HTTP_REFERER'])
    if success == True:
        messages.success(request, "Inclusão de apelido com sucesso")
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, error_message)
        return redirect(request.META['HTTP_REFERER'])

def agoraconfiguracaoemail(request):
    us = User.objects.get(user=request.user)
    user = us.user
    email = request.POST['text-email']
    if email:
        email_user = User.objects.get(user=user)
        email_user.email = email
        email_user.save()
        success = True
    else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
        return redirect(request.META['HTTP_REFERER'])
    if success == True:
        messages.success(request, "Inclusão de email com sucesso")
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, error_message)
        return redirect(request.META['HTTP_REFERER'])

def agoraconfiguracaoapelidoremove(request):
    us = User.objects.get(user=request.user)
    user = us.user
    apelido_user = User.objects.get(user=user)
    apelido_user.nickname = user.user.primeiro_nome
    apelido_user.save()

    success = True
    if success == True:
        messages.success(request, "Apelido excluido com sucesso")
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, error_message)
        return redirect(request.META['HTTP_REFERER'])
